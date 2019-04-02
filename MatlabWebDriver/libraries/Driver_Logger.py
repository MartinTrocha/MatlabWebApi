import logging
import pathlib
import datetime

class Driver_Logger(object):

    def __init__(self):
        self.CONST_PATH_LOGFILE_DIR = "/home/martin/MatlabWebDriver/logs"

        try:
            pathlib.Path(self.CONST_PATH_LOGFILE_DIR).mkdir(mode=0o777, parents=True, exist_ok=True)
            path = self.CONST_PATH_LOGFILE_DIR+"/logs.txt"
            logging.basicConfig(filename=path, level=logging.DEBUG)
            logging.info("Matlab Web API Logger Started: " + "{:%B %d, %Y}".format(datetime.datetime.now()))


        except FileExistsError as e:
            print(e.strerror)
            logging.info("Failed to create and load logfile")
            raise


    def log(self, lines, tag, _type):
        if _type == "warning":
            logging.warning("Matlab Web API Logger: "+tag+" "+str(datetime.datetime.now())+" : "+lines+"\n")
        elif _type == "error":
            logging.error("Matlab Web API Logger: "+tag+" "+str(datetime.datetime.now())+" : "+lines+"\n")
        else:
            logging.info("Matlab Web API Logger: " + tag + " " + str(datetime.datetime.now()) + " : " + lines + "\n")
