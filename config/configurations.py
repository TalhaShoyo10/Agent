import os
from dotenv import load_dotenv
from agent.llm import get_gemini
from tavily import TavilyClient
from pinecone import Pinecone , ServerlessSpec
from rag.embeddings import get_embeddings

load_dotenv()

#Embedding Instantiation
EMBEDDING_MODEL = get_embeddings()

#LLM Instantiation
LLM_Reasoning = get_gemini(0.3 , "gemini-3-flash-preview")
LLM_OCR = get_gemini(0.1 , "gemini-2.5-flash-lite")

#Vector Database Instantiation
pinecone_api = os.getenv("PINECONE_API_KEY")
if pinecone_api is None :
    raise ValueError("PINECONE_API_KEY is not a valid environment variable") 
INDEX_NAME = "little-angels-rag-index"
PINECONE_CLIENT= Pinecone(api_key = pinecone_api)
existing_indices = [index.name for index in PINECONE_CLIENT.list_indexes()]
if INDEX_NAME not in existing_indices :
    PINECONE_CLIENT.create_index(name = INDEX_NAME , dimension = 384 , metric = "cosine" , spec = ServerlessSpec(cloud="aws" , region="us-east-1"))

#Tavily Instantiation
tavily_api = os.getenv("TAVILI_API_KEY")
if tavily_api is None :
    raise ValueError("TAVILI_API_KEY is not a valid environment variable")
TAVILY_CLIENT = TavilyClient(tavily_api)