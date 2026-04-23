from sources.logger import logging
from sources.exception import CustomException

import os
import sys
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

class LLM_Model:
    def __init__(self, Model = "llama-3.1-8b-instant", api_key = os.getenv("GROQ_API_KEY"), temperature = 0.3):
        try:
            self.llm = ChatGroq(model_name=Model, api_key=api_key, temperature=temperature)
            logging.info("LLM Model initialized successfully")
        except Exception as e:
            logging.error("Error in initializing LLM Model")
            raise CustomException(e, sys)
    
    def generate_response(self, prompt):
        try:
            response = self.llm.invoke(prompt)
            logging.info("Response generated successfully")
            return response
        except Exception as e:
            logging.error("Error in generating response")
            raise CustomException(e, sys)   
        