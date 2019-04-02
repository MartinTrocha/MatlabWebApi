import syslog
from libraries import Driver_Logger

class Driver_Main(object):

    def __init__(self, _logger = None):
        self._logger = _logger

        if self._logger is None:
            self._logger = Driver_Logger.Driver_Logger()

    def log(self, lines, tag, type):
        self._logger.log(lines, tag, type)











'''
class Driver_Main(object):

    def __init__(self):
        self.CONST_TAG = "[DRIVER MAIN]"
        self.__autoload()


    def __autoload(self):
        try:
            self._driver_logger = Driver_Logger.MWBLogger()
            self._driver_instance = Driver_Instance.InstanceDriver()
            self._driver_matlab = Driver_MatlabCode.MatlabCode()
            self._driver_webcommunication = Driver_WebCommunication.WebCommDriver()
        except Exception as e:
            self._driver_logger = None
            self._driver_instance = None
            self._driver_matlab = None
            self._driver_webcommunication = None


    @property
    def logger(self):
        return self._driver_logger

    @property
    def instance(self):
        return self._driver_instance

    @property
    def matlab(self):
        return self._driver_matlab

    @property
    def webcommunication(self):
        return self._driver_webcommunication

    def run(self):
        if self.logger is None:
            syslog.syslog(self.CONST_TAG+' Logger is not loaded\n')

        if self.webcommunication is None:
            if self.logger is not None:
                self.logger.log(self.CONST_TAG+' Web Communication failed to load\n')
            else:
                syslog.syslog(self.CONST_TAG+' Web Communication failed to load\n')
            return

        if self.instance is None:
            if self.logger is not None:
                self.logger.log(self.CONST_TAG+' Matlab instances failed to load\n')
            else:
                syslog.syslog(self.CONST_TAG+' Matlab instances failed to load\n')
            return

        if self.instance is None:
            if self.logger is not None:
                self.logger.log(self.CONST_TAG + ' Matlab instances failed to load\n')
            else:
                syslog.syslog(self.CONST_TAG + ' Matlab instances failed to load\n')
            return

        if self.matlab is None:
            if self.logger is not None:
                self.logger.log(self.CONST_TAG + ' Matlab code executioner failed to load\n')
            else:
                syslog.syslog(self.CONST_TAG + ' Matlab code executioner failed to load\n')
            return

        self.webcommunication.run()'''

'''class MainDriver:

    def __init__(self):
        self.CONST_TAG = "[MainDriver]"

    def __autoload(self):
        try:
            self.config = app.CONFIG
        except Exception as e:
            print(e)
            exit(1)

        self.logger = Driver_Logger.MWBLogger()
        self.driver_instance = Driver_Instance.InstanceDriver(logger=self.logger)
        self.driver_code = Driver_MatlabCode.MatlabCode(logger=self.logger)
        self.driver_webcommunication = Driver_WebCommunication.WebCommDriver(logger=self.logger,
                                                                             instance_driver=self.driver_instance,
                                                                             URL=self.config.get("URL"), PORT=self.config.get("PORT"))

        self.logger.log("Main Driver Initialized", tag=self.CONST_TAG, _type='info')

    def run(self):
        self.__autoload()
        self.driver_webcommunication.run()'''






'''eng = main_driver.instance_driver.create_default_matlab_instances()
instance = main_driver.instance_driver.get_free_instance()
instance.simulink2(nargout=0)'''




'''eng = main_driver.instance_driver.create_default_matlab_instances()
instance = main_driver.instance_driver.get_free_instance()

#result  = main_driver.code_driver.run_file(instance, 'test', 84.0)
result = main_driver.code_driver.simulink(instance, True)

f = open('/home/martin/MatlabWebDriver/result.txt', 'a')
f.writelines(str(result)+"\n")
f.close()'''



