import os
from libraries.Driver_Main import Driver_Main
from libraries.Main_RequestHandler import *

import ssl

class WebCommDriver(Driver_Main):
    def __init__(self):
        Driver_Main.__init__(self)

        self.CONST_TAG = "[WEB COMMUNICATION]"

    @property
    def URL(self):
        return self._URL

    @property
    def PORT(self):
        return self._PORT

    @property
    def server(self):
        return self._server

    @property
    def request(self):
        return self._request

    '''
        Set URL and PORT
    '''
    def setup_connection_params(self, URL, PORT):
        self._URL = URL
        self._PORT = PORT
        Driver_Main.log(self, "URL and PORT set up", self.CONST_TAG, None)


    '''
        Set up Server with Request handler
    '''
    def init_server(self):
        self._request = HTTP_SERVER
        self._request.server_version = ""
        self._request.sys_version = ""

        self._server = ThreadedServer((self._URL, self._PORT), self._request)
        Driver_Main.log(self, "SERVER INIT SUCCESSFULLY", self.CONST_TAG, None)


    '''
        Run web communication
    '''
    def run(self, URL, PORT):
        try:
            self.setup_connection_params(URL, PORT)
            self.init_server()

            Driver_Main.log(self, lines="Starting server...", tag=self.CONST_TAG, type=None)
            self._server.serve_forever()
        except Exception as e:
            Driver_Main.log(self, e.__str__(), self.CONST_TAG, None)
            Driver_Main.log(self, "Server failed to start", self.CONST_TAG, None)
            raise



















































    '''def __init__(self, logger = None, instance_driver = None, URL = None, PORT = None):
        self.CONST_TAG = "[MatlabWeb]"
        self.instance_driver = instance_driver

        self.base_path = os.path.dirname(__file__) + '/server'



    def run(self):

        if(self.logger is None):
            pass

        if(self.URL is None or self.PORT is None):
            return

        if(self.instance_driver is None):
            return

        try :
            server = Main_RequestHandler.ThreadedServer((self.URL, self.PORT), Main_RequestHandler.HTTP_SERVER)
            server.serve_forever()
        except Exception as e:
            self.logger.log('kokotina', 'ERROR', 'ERROR')

        #server = ThreadedServer((self.URL, self.PORT), self.handler_http_server)
        #print('Server started')
        #server.serve_forever()'''






























'''
class HTTP_SERVER(http.server.BaseHTTPRequestHandler):

    def _set_headers(self, err_code = 404):
        self.send_response(err_code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/html')
        #self.send_header('Content-Length')
        self.end_headers()

    def do_GET(self):
        path = urllib.parse.urlparse(self.path)
        self._set_headers(200)
        self.wfile.write("GET request for {} <br>".format(self.path).encode('utf-8'))


    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <-- size of data
        post_data = self.rfile.read(content_length)  # <-- data itself

        self._set_headers()
        self.wfile.write("POST request for {}".format(post_data).encode('utf-8'))

   


class ThreadedServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """lalala"""'''