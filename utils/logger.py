import logging
import os
import traceback

class Logger():

    def setLogger(self):
        logDirectory = "logs"
        logFilename = "app.log"

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logPath = os.path.join(logDirectory, logFilename)
        fileHandler = logging.FileHandler(logPath, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fileHandler.setFormatter(formatter)

        if(logger.hasHandlers()):
            logger.handlers.clear()
        logger.addHandler(fileHandler)
        return logger
    
    @classmethod
    def addToLog(cls, level, message):
        try:
            logger = cls.setLogger(cls)

            if (level == "critical"):
                logger.critical(message)
            elif (level == "debug"):
                logger.debug(message)
            elif (level == "error"):
                logger.error(message)
            elif (level == "info"):
                logger.info(message)
            elif (level == "warn"):
                logger.warn(message)
        except Exception as ex:
            print(traceback.format_exc())
            print(ex)