from config.configurations import PINECONE_CLIENT , INDEX_NAME , EMBEDDING_MODEL
from langchain_pinecone import PineconeVectorStore

namespace_cache = {}

def get_namespace(name_space : str = None) :
    cache_key = name_space or "default"
    
    if cache_key not in namespace_cache : 
        namespace_cache[cache_key] = PineconeVectorStore(index = PINECONE_CLIENT.Index(INDEX_NAME) , embedding = EMBEDDING_MODEL , namespace = name_space)

    return namespace_cache[cache_key]


    



