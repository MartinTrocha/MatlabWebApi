from libraries import JSONRPCExceptions
from libraries import JSONRPCErrorResponse

import json
import inspect

class JSONRPC(object):

    def __init__(self, request):
        self.request = request


    # Not valid JSON object throws ParseError
    def _load_from_json(self):
        try:
            self.request = json.loads(self.request)
        except ValueError:
            raise JSONRPCExceptions.ParseError()

    # Not valid JSON RPC object throws InvalidRequest
    def _validate(self):
        try:
            self._load_from_json()
        except JSONRPCExceptions.ParseError():
            raise JSONRPCExceptions.ParseError()

        if not self.request['jsonrpc'] or self.request['jsonrpc'] != '2.0':
            raise JSONRPCExceptions.InvalidRequest()

        if not self.request['id']:
            raise JSONRPCExceptions.InvalidRequest()

        if not self.request['params']:
            raise JSONRPCExceptions.InvalidRequest()

        if not self.request['method']:
            raise  JSONRPCExceptions.InvalidRequest()

    def dispatch(self, controller):
        exception = None
        try:
            self._validate()
        except JSONRPCExceptions.InvalidRequest():
            exception = JSONRPCExceptions.InvalidRequest()
        except JSONRPCExceptions.ParseError():
            exception = JSONRPCExceptions.ParseError()

        if exception is not None:
            response = JSONRPCErrorResponse.JSONRPCErrorResponse(request_id=self.request['id'], code=exception.code, message=exception.message)
            return response


        func = controller.__dict__[self.request['method']]

        method_inspect = inspect.getfullargspec(func)
        if len(method_inspect.args) > 1:
            err, val = func(controller, self.request['params'])
        else:
            err, val = func(controller)

        return {
            'id': self.request['id'],
            'result': {
                'status': err,
                'value': val
            },
            'jsonrpc': '2.0'
        }