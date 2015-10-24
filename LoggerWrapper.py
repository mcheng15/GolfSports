import logging 

class LoggerWrapper(object):
    """LogWrapper"""

    def __init__(self): 
        logging.basicConfig(filename = 'golf_log.txt', level = logging.DEBUG)
        
    def LogWarningMessage(self, msg):
         logging.warning(msg)


