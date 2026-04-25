import uuid
import logging
import asyncio
from rag.chunker import chunking_per_upload
from config.configurations import EMBEDDING_MODEL , INDEX_NAME , PINECONE_CLIENT
from langchain_pinecone import PineconeVectorStore

async def generate_unique_session_id() -> str :
    loop = asyncio.get_event_loop()
    index = PINECONE_CLIENT.Index(INDEX_NAME)
    
    stats = await loop.run_in_executor(None, index.describe_index_stats)
    existing_namespaces = stats['namespaces'].keys()

    session_id = str(uuid.uuid4())
    while session_id in existing_namespaces:
        session_id = str(uuid.uuid4())

    return session_id

def ingest_uploaded_docs(docs , session_id : str) :
    chunks = chunking_per_upload(docs)
    
    if not chunks:
        print("No parsable content exists.")
        return 
    
    PineconeVectorStore.from_documents(documents = chunks , embedding = EMBEDDING_MODEL , index_name = INDEX_NAME, namespace = session_id)


def delete_session_vectors(session_id : str) :
    try:
        index = PINECONE_CLIENT.Index(INDEX_NAME)
        index.delete(delete_all=True, namespace=session_id)
    except Exception as e:
        #session never uploaded files so nothing to delete
        if "Namespace not found" in str(e):
            pass  
        else:
            logging.error(f"Failed to delete vectors for session {session_id}: {e}")