import logging 
import os

LOG_FILE_NAME = "C:/logs/golf_log.txt"

class LoggerWrapper(object):
    """LogWrapper"""

    def __init__(self):
        if(os.path.isfile(LOG_FILE_NAME)):
            os.remove(LOG_FILE_NAME)
        open(LOG_FILE_NAME, 'a').close()
        logging.basicConfig(filename = 'C:/logs/golf_log.txt', level = logging.DEBUG)
        
    def LogWarningMessage(self, msg):
         logging.warning(msg)

    def LogErrorMessage(self, msg):
        logging.error(msg);


