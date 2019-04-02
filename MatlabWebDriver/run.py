#!/usr/bin/python3

from libraries.Driver_WebCommunication import WebCommDriver
from libraries.Driver_Instance import InstanceDriver
from configs.app import CONFIG

class APP(object):

    def __init__(self):
        self.matlab_intances = InstanceDriver()
        self.web = WebCommDriver()

    def run(self):
        self.matlab_intances.create_default_matlab_instances()
        self.web.run(URL=CONFIG['URL'], PORT=CONFIG['PORT'])


app = APP()
app.run()