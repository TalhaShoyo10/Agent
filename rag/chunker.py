import json 
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunking(json_file : str = "cleaned_text.json") :
    documents = []
    with open(json_file , "r" , encoding="utf-8") as file :
        parsed_text = json.load(file)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 200 , chunk_overlap = 50)
    
    for instance in parsed_text :
        document = text_splitter.create_documents([instance["content"]] , metadatas = [{"source" : instance["source"]}])
        documents.extend(document)
    
    return documents

def chunking_per_upload(docs) :
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 512 , chunk_overlap = 50)
    chunks = text_splitter.split_documents(documents = docs)
    return chunks
    
    