from sources.logger import logging
from sources.exception import CustomException
from sources.Model.model import LLM_Model
import sys


def main():
    try:
        logging.info("Starting the application")
        model = LLM_Model()
        prompt = "create a quiz for python subject with 10 questions and when I completed plesae give me feedback about quiz results"
        response = model.generate_response(prompt)
        print(response.content)

    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)   


if __name__ == "__main__":
    main()
