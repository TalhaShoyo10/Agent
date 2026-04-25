import os
import logging
from dotenv import load_dotenv
from config.configurations import TAVILY_CLIENT
from rag.get_namespace import get_namespace
from langchain.tools import tool

load_dotenv()

logging.basicConfig(
    filename="agent_calls.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_tool_call(tool_name: str, query: str, output: str):
    logging.info(f"Tool: {tool_name} , Query: {query} , Output: {str(output)[:100]}....")


@tool(
    description="""
    Use this tool for:
    - Current events
    - News
    - Information NOT found in internal documents
    - Questions unrelated to Little Angels Montessori
    """
)
def web_search(user_query: str) -> str:
    api_key = os.getenv("TAVILI_API_KEY")

    if api_key is None:
        raise ValueError("TAVILI_API_KEY is not a valid environment variable")

    try:
        tavily_client = TAVILY_CLIENT
        response = tavily_client.search(query=user_query, max_results=2)

        str_list = []
        for i in range(len(response["results"])):
            str_list.append(f"RESULT {i}: " + response["results"][i]["content"])

        result_text = "\n\n".join(str_list) if str_list else "No relevant web results found."
    except Exception as e:
        result_text = "Sorry, I can not retrieve external information at the moment."
        logging.error(f"Web search failed for query '{user_query}': {e}")

    log_tool_call("web_search", user_query, result_text)
    return result_text


def deploy_relevant_internal_search(session_id: str = None):
    def internal_knowledge_lookup(
        user_query: str,
        uploaded_doc_only: bool = False,
        source_filter: str = None,
        top_k: int = 4,
        max_results: int = 2
    ) -> dict:
        if uploaded_doc_only and session_id is not None:
            namespaces = [session_id]
        else:
            namespaces = [None]
            if session_id is not None:
                namespaces.insert(0, session_id)

        retrieved_results = []

        try:
            for namespace in namespaces:
                results_with_scores = get_namespace(namespace).similarity_search_with_score(query=user_query , k=top_k)
                
                if source_filter is not None:
                    results_with_scores = [(doc, score) for doc , score in results_with_scores if doc.metadata.get("source") == source_filter]
                retrieved_results.extend(results_with_scores)
                
        except Exception as e:
            logging.error(f"RAG retrieval failed for query '{user_query}': {e}")
            output = {
                "found": False,
                "error": True,
                "context": "",
                "sources": [],
                "message": "I am sorry, I can not retrieve information from internal documents at the moment."
            }
            log_tool_call("internal_knowledge_search", user_query, output)
            return output

        relevant_results = [doc for doc, score in retrieved_results if score > 0.3][:max_results]

        if not relevant_results:
            output = {"found": False , "error": False , "context": "" , "sources": [] , "message": "No relevant information found in internal documents."}
            log_tool_call("internal_knowledge_search", user_query, output)
            return output

        context = "\n\n".join(doc.page_content for doc in relevant_results)
        sources = [doc.metadata.get("source", "unknown") for doc in relevant_results]

        output = {"found": True ,"error": False , "context": context , "sources": sources , "message": "Relevant internal information found."}
        log_tool_call("internal_knowledge_search", user_query, output)
        return output

    @tool(
        description="""
        PRIMARY INTERNAL KNOWLEDGE TOOL:

        Use this tool when:
        - The user has uploaded documents in this session
        - The query may relate to uploaded documents
        - The question is about Little Angels Montessori

        This includes:
        - School name and description
        - Monthly fees (Nursery, Prep, KG)
        - School timings
        - Summer camp dates, timings, and fees
        - Any information explicitly present in internal school documents
        - Any information from documents uploaded by the user

        PRIORITY RULE:
        - If the user has uploaded documents, you should strongly prefer this tool
        - If there is a reasonable chance the answer exists in internal documents, try this tool first

        DO NOT use this tool if:
        - The query is clearly about current events or news
        - The query is unrelated to the school or uploaded documents
        """
    )
    def internal_knowledge_search(user_query: str) -> str:
        result = internal_knowledge_lookup(user_query)

        if not result["found"]:
            return result["message"]

        return (
            "INTERNAL DOCUMENT CONTEXT:\n"
            f"{result['context']}\n\n"
            "SOURCES:\n"
            f"{', '.join(result['sources'])}"
        )

    return internal_knowledge_search, internal_knowledge_lookup
