import os 
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_gemini(temp : int , model : str = "gemini-3-flash-preview") :
  gemini_api = os.getenv("GEMINI_API_KEY")

  if gemini_api is None :
   raise ValueError("GEMINI_API_KEY is not a valid environment variable.")

  base_model = ChatGoogleGenerativeAI(model = model , google_api_key = gemini_api , temperature = temp)
   
  return base_model


