import time
import threading
import gradio as gr
from agent.agent_setup import get_agent, agent_cache
from agent.tools import deploy_relevant_internal_search, web_search
from rag.get_namespace import namespace_cache
from rag.input_extraction import content_extraction
from rag.upload_ingest import (
    ingest_uploaded_docs,
    delete_session_vectors,
    generate_unique_session_id
)
from langchain_core.messages import HumanMessage, SystemMessage
from pathlib import Path

ingested_files = {}
session_uploaded_sources = {}
last_active = {}


def expired_session_cleaning():
    while True:
        time.sleep(300)

        now = time.time()
        expired_sessions = [
            sess_id for sess_id, last_active_time in last_active.items()
            if (now - last_active_time) > 600
        ]

        for sess_id in expired_sessions:
            delete_session_vectors(sess_id)
            ingested_files.pop(sess_id, None)
            session_uploaded_sources.pop(sess_id, None)
            last_active.pop(sess_id)
            agent_cache.pop(sess_id, None)
            namespace_cache.pop(sess_id, None)


def is_uploaded_doc_request(user_query: str) -> bool:
    query = user_query.lower()

    triggers = [
        "uploaded document",
        "uploaded file",
        "this document",
        "this file",
        "the pdf",
        "the uploaded pdf",
        "summarize the document",
        "summarize the uploaded document",
        "summary of the uploaded document",
        "summary of the document",
        "summarize this document",
        "summarize this file",
        "summary of this file",
        "what is in the uploaded file",
        "what is in this document",
        "what does this document say",
        "give me summary of the uploaded document"
    ]

    return any(trigger in query for trigger in triggers)


Cleanup_thread = threading.Thread(target=expired_session_cleaning, daemon=True)
Cleanup_thread.start()


async def chat_function(user_input, history, files, session_id):
    if history is None:
        history = []

    has_input = user_input and user_input.strip()
    has_files = files is not None and files != []

    if not has_input and not has_files:
        yield history, "", session_id
        return

    history.append({
        "role": "user",
        "content": user_input if has_input else "Uploaded document(s)"
    })
    history.append({
        "role": "assistant",
        "content": "📄 Processing uploaded documents...." if has_files else "⏳ Thinking...."
    })
    yield history, "", session_id

    if session_id is None:
        session_id = await generate_unique_session_id()

    last_active[session_id] = time.time()

    if has_files:
        already_ingested = ingested_files.get(session_id, set())
        new_files = [file for file in files if file.name not in already_ingested]

        if new_files:
            docs = content_extraction(new_files)
            ingest_uploaded_docs(docs, session_id)

            for file in new_files:
                already_ingested.add(file.name)

            ingested_files[session_id] = already_ingested
            session_uploaded_sources[session_id] = [file.name for file in new_files]

    if not has_input:
        history[-1]["content"] = "Document(s) uploaded successfully! Ask me anything about them."
        yield history, "", session_id
        return

    history[-1]["content"] = "⏳ Thinking...."
    yield history, "", session_id

    user_query = user_input.strip()
    has_uploaded_docs = session_id in ingested_files and len(ingested_files[session_id]) > 0
    uploaded_doc_request = is_uploaded_doc_request(user_query)

    if has_uploaded_docs:
        _, internal_lookup = deploy_relevant_internal_search(session_id)

        if uploaded_doc_request:
            latest_sources = session_uploaded_sources.get(session_id, [])
            source_filter = latest_sources[-1] if latest_sources else None

            internal_result = internal_lookup(
                user_query="main ideas, key arguments, important points, summary, conclusion",
                uploaded_doc_only=True,
                source_filter=source_filter,
                top_k=10,
                max_results=6
            )

            if internal_result["found"]:
                context_block = (
                    "You are answering about a user-uploaded document.\n"
                    "Use only the uploaded document context below.\n"
                    "Do not use Little Angels Montessori background knowledge unless the user explicitly asks for it.\n"
                    "If the user asks for a summary, provide a concise but informative summary of the uploaded document.\n\n"
                    f"{internal_result['context']}\n\n"
                    f"SOURCES: {', '.join(internal_result['sources'])}"
                )
            else:
                context_block = (
                    "The user asked about an uploaded document, but no relevant uploaded-document context was found.\n"
                    "Tell the user clearly that the uploaded document content could not be retrieved."
                )

            agent = get_agent(session_id)
            response = await agent.ainvoke({
                "messages": [
                    SystemMessage(content=context_block),
                    HumanMessage(content=user_query)
                ]
            })
        else:
            internal_result = internal_lookup(
                user_query=user_query,
                uploaded_doc_only=False,
                top_k=4,
                max_results=2
            )

            if internal_result["found"]:
                context_block = (
                    "Use the following internal document context to answer the user.\n"
                    "Prefer uploaded document context when it is available and relevant.\n\n"
                    f"{internal_result['context']}\n\n"
                    f"SOURCES: {', '.join(internal_result['sources'])}"
                )
            else:
                web_result = web_search.invoke(user_query)
                context_block = (
                    "Internal retrieval found no relevant context.\n"
                    "Use the following web results to answer the user.\n\n"
                    f"{web_result}"
                )

            agent = get_agent(session_id)
            response = await agent.ainvoke({
                "messages": [
                    SystemMessage(content=context_block),
                    HumanMessage(content=user_query)
                ]
            })
    else:
        agent = get_agent(session_id)
        response = await agent.ainvoke({
            "messages": [HumanMessage(content=user_query)]
        })

    ai_text = response["messages"][-1].content[0]["text"]
    history[-1]["content"] = ai_text
    yield history, "", session_id


graphics_dir = Path(__file__).parent.parent / "graphics"

with gr.Blocks() as demo:
    with gr.Row(elem_id="title-row"):
        gr.Image(
            value=str(graphics_dir / "logo.png"),
            elem_id="school-logo",
            show_label=False,
            container=False,
            width=80,
            height=80,
            interactive=False,
            show_download_button=False,
            show_fullscreen_button=False,
        )
        gr.Markdown(
            "# Little Angels Montessori Assistant\nAsk about school timings, admissions and any other details you are curious about",
            elem_id="app-title"
        )

    session_id = gr.State(None)
    chatbot = gr.Chatbot(height=400, show_label=False, elem_id="chat-history")

    with gr.Row(elem_id="input-row"):
        file_upload = gr.UploadButton(
            label="📎Upload",
            file_types=[".pdf", ".txt", ".png", ".jpg", ".jpeg"],
            file_count="multiple",
            elem_id="file-upload",
            scale=0
        )
        user_input = gr.Textbox(placeholder="Type your question here...",lines=1,elem_id="chat-input",show_label=False,scale=10)

    user_input.submit(chat_function , [user_input, chatbot, file_upload, session_id] ,[chatbot, user_input, session_id]) 
    file_upload.upload(
        chat_function,
        [user_input, chatbot, file_upload, session_id],
        [chatbot, user_input, session_id]
    )
