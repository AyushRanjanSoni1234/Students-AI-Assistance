from sources.logger import logging
from sources.exception import CustomException
from sources.Model.model import LLM_Model
import sys


def main():
    try:
        logging.info("Starting the application")
        model = LLM_Model()
        prompt = "Tell me about the history of artificial intelligence"
        response = model.generate_response(prompt)
        print(response.content)

    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)   


if __name__ == "__main__":
    main()
