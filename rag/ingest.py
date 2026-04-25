from rag.chunker import chunking
from config.configurations import EMBEDDING_MODEL , INDEX_NAME
from langchain_pinecone import PineconeVectorStore
from pathlib import Path
import hashlib

def hash_func(doc) :
    raw_str = f"{doc.metadata.get("source")} :: {doc.page_content}"
    return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

def ingest(json_file : str = "cleaned_text.json") :
    root_dir = Path(__file__).parent.parent
    documents = chunking(root_dir / json_file)
    ids = [hash_func(doc) for doc in documents]
    PineconeVectorStore.from_documents(documents = documents , embedding = EMBEDDING_MODEL , index_name = INDEX_NAME , ids = ids)
    
    print(f"{len(documents)} documents ingested into Pinecone Index : ({INDEX_NAME})")
    
if __name__ == "__main__" :
    ingest()