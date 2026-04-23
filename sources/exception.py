import sys
from sources.logger import logging

class CustomException(Exception):
    def __init__(self, error_message, error_details:sys):
        self.error_message = error_message
        _,_,exc_tb  = error_details.exc_info()

        self.line_number = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occurred in file: {self.file_name} at line number: {self.line_number} with error message: {self.error_message}"
    
if __name__ == "__main__":
    try:
        logging.info("This is an Error message")
        a = 2/0
        print("This will not be diveded by zero")
    except Exception as e:
        raise CustomException(e, sys)