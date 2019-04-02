
class JSONRPCErrorResponse():

    def __init__(self, request_id, code, message):
        super(JSONRPCErrorResponse, self).__init__({
            {
                "jsonrpc": "2.0",
                "error": {"code": code, "message": message},
                "id": request_id,
            }
        })