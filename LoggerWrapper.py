import logging
import sys
import os
sys.path.append("Infrastructure/")

FORMAT = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
FileHandler = None
StreamHandler = None

def InitializeLogger(loggerName, fileName):
    global FileHandler, StreamHandler

    #create
    log = logging.getLogger(loggerName)
    log.setLevel(logging.DEBUG)

    stdOutHandler = logging.StreamHandler(sys.stdout)
    stdOutHandler.setFormatter(FORMAT)
    log.addHandler(stdOutHandler)

    fileHandler = logging.FileHandler(fileName)
    fileHandler.setFormatter(FORMAT)
    log.addHandler(fileHandler)

def GetLogger(name):
    return logging.getLogger(name)

