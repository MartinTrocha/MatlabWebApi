import re
import importlib
import logging
import inspect

import json

from configs.routes import ROUTES
from libraries import JSONRPCObject
from configs.app import CONFIG

class Router(object):

    def __init__(self, server):
        self.CONST_PATH_LOGFILE_DIR = CONFIG['BASEPATH']+"logs"
        self._server = server
        self._routes = ROUTES
        path = self.CONST_PATH_LOGFILE_DIR + "/logs.txt"
        logging.basicConfig(filename=path, level=logging.DEBUG)

    def add_route(self, regexp, controller, action):
        self._routes.append({'expression': regexp, 'controller': controller, 'action': action})

    def get_routes(self):
        return self._routes

    def return_error(self, error_code=404, message=""):
        self._server.send_error(error_code, message)
        self._server.end_headers()


    def _output(self, error_code, data, _json = False):
        self._server.send_response(error_code)
        if _json:
            self._server.send_header('Content-type', 'application/json')
        else:
            self._server.send_header('Content-type', 'text/html')

        self._server.send_header('Access-Control-Allow-Origin', '*')
        self._server.end_headers()

        if _json:
            self._server.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            self._server.wfile.write(str(data).encode('utf-8'))

    def route(self, path, data, json_rpc = False):
        for route in ROUTES:
            if re.search(route['expression'], path):
                try:
                    # load module
                    module = importlib.import_module(route['controller'])
                except ImportError as ErrorImport:
                    print(ErrorImport.__str__())
                    self.return_error(500)
                    raise

                try:
                    # load controller
                    className = route['controller'].split('.')
                    className = className[len(className) - 1]
                    controller = getattr(module, className)
                except UnboundLocalError as ErrorLocalUnbound:
                    print(ErrorLocalUnbound.__str__())
                    self.return_error(500)
                    raise

                try:
                    # init controller
                    controller.__init__(controller, self._server)
                except TypeError as ErrorType:
                    print(ErrorType.__str__())
                    self.return_error(500)
                    raise

                if json_rpc:
                    self._output(200, "In development", True)
                    return
                    response = JSONRPCObject.JSONRPC(data).dispatch(controller=controller)
                    self._output(200, response, True)
                    return
                else:
                    try:
                        # load function
                        func = controller.__dict__[route['action']]

                        method_inspect = inspect.getfullargspec(func)
                        if len(method_inspect.args) > 1:
                            err_code, retval = func(controller, data)
                        else:
                            err_code, retval = func(controller)
                        self._output(err_code, retval)

                    except KeyError as ErrorKey:
                        print(ErrorKey.__str__())
                        self.return_error(405)
                        raise
                return

        self.return_error(404)



