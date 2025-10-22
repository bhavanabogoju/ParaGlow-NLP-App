# src/exception.py
import sys
from src.logger import logger

def get_error_details(error, error_detail:sys):
    """
    Returns a formatted error message with file name and line number.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = f"Error occurred in python script name [{file_name}] line number [{line_number}] error message [{str(error)}]"
    return error_message

class CustomException(Exception):
    """
    Custom exception class.
    """
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = get_error_details(error_message, error_detail=error_detail)

        # Log the error as soon as the exception is raised
        logger.error(self.error_message)

    def __str__(self):
        return self.error_message