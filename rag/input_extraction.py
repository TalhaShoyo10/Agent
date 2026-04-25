import os 
import requests
from pypdf import PdfReader
from config.configurations import LLM_OCR
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

def content_extraction(input_files) :
    docs = []
    
    for file in input_files :
        filename = file.name
        
        if filename.lower().endswith(".txt") :
            with open(file.name, "r") as f:
                text = f.read()
            docs.append(Document(page_content = text, metadata = {"source": file.name}))
            
        elif filename.lower().endswith(".pdf") :
            reader = PdfReader(file.name)
            for i, page in enumerate(reader.pages):
                docs.append( Document(page_content=page.extract_text(), metadata={"source": file.name, "page": i}))
                
        elif filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg") or filename.lower().endswith(".png") :
            ocr_api = os.getenv("OCR_API_KEY")
            extracted_text = []
            cleaned_text = []
            
            instructions = {'isOverlayRequired': False , 'apikey': ocr_api , 'language': "eng" }
            with open(filename , "rb") as file :
                request = requests.post(url ='https://api.ocr.space/parse/image', files = {"image" : file}, data = instructions)
            
            request_json = request.json()
            if request_json['IsErroredOnProcessing']  == False :
               extracted_text.append({"content" : request_json['ParsedResults'][0]['ParsedText'] , "source" : filename})
            else :
                print(f"OCR tool failed to extract the text from {filename}")
                
            cleaning_llm = LLM_OCR
    
            for entry in extracted_text :
                prompt = f""" You are cleaning OCR-extracted text.
                            Rules:
                                - Fix obvious OCR spelling errors.
                                - Merge broken lines into natural sentences.
                                - Preserve all information.
                                - Do NOT add new information.
                                - Do NOT remove phone numbers, dates, addresses, or emails.
                                - Do NOT summarize or rewrite marketing language.
                                - REMOVE any marketing language similar to phrases like avail an anmazing discount or born to shine
                                - Keep the original meaning and structure.

                                Return ONLY the cleaned text.

                                OCR Text:
                                ---
                                    {entry["content"]}
                                --- """
                response = cleaning_llm.invoke(input = prompt)
                cleaned_text.append({"content" : response.content , "source" : entry["source"]})
            
            for entry in cleaned_text :  
                docs.append(Document(page_content = entry["content"] , metadata = {"source": entry["source"]}))
    
    return docs