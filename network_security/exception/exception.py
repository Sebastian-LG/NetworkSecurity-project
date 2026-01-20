import sys
from network_security.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    #Overwrite the str method
    def __str__(self):
        return f"Error ocurred in python script name [{self.filename}] line number [{self.lineno}] error message [{self.error_message}]"


#if __name__ == "__main__":
#    try:
#        logger.logging.INFO("Enter the try block")
#        a = 1/0
#    except Exception as e:
#        logger.logging.info("Enter the except block")
#        raise NetworkSecurityException(e,sys)

