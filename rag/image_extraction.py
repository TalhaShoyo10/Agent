import os
import re
import json
from config.configurations import LLM_OCR
from dotenv import load_dotenv
import requests

load_dotenv()

def image_extraction_cleaning(cleaned_output_file : str = "cleaned_text.json") :
    
    extracted_text = []
    cleaned_text = []
    finalised_text = []
    #filenames = []
    ocr_api = os.getenv("OCR_API_KEY")
    IMAGE_DIR = "images"

    for filename in os.listdir(IMAGE_DIR) :
        if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg") or filename.lower().endswith(".png") :
            image_path = os.path.join(IMAGE_DIR , filename)
            #filenames.append(filename)
            
            instructions = {'isOverlayRequired': False , 'apikey': ocr_api , 'language': "eng" }
            with open(image_path , "rb") as file :
                request = requests.post(url ='https://api.ocr.space/parse/image', files = {filename: file}, data = instructions)
            
            request_json = request.json()
            if request_json['IsErroredOnProcessing']  == False :
               extracted_text.append({"content" : request_json['ParsedResults'][0]['ParsedText'] , "source" : filename})
            else :
                print(f"OCR tool failed to extract the text from {filename}")
    
    extracted_text.append({"content" : "Classes offered : Kindergarten , Prep and Nursery. Monthly fees : 8000 Rupees(Prep) , 6000 Rupees (Kindergarten and Nursery)" , "source" : "manual_entry"})
    
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
        entry["content"] = re.sub(r"(\d{1,2}[.:]\d{2})\s*-\s*(\d{1,2}[.:]\d{2})" , lambda match : f"{match.group(1)} AM - {match.group(2)} PM" , entry["content"] )
        entry["content"] = re.sub(r"2025" , "2026" , entry["content"])
        entry["content"] = re.sub(r'\b(?:main\s+)?double\s+road\b' , 'Main Double Road', entry["content"] , flags = re.IGNORECASE)
        entry["content"] = re.sub(r"Sector\s+[A-Z0-9/\-–—]{2,8}" , "Sector I-8/4" , entry["content"] , flags = re.IGNORECASE)
        finalised_text.append({"content" : entry["content"] , "source" : entry["source"]})
        
    with open(cleaned_output_file , "w" , encoding = "utf-8") as json_file :
        json.dump(finalised_text , json_file , ensure_ascii = False, indent = 4)


image_extraction_cleaning()




