import http.server
import socketserver
import urllib.parse
import cgi

from libraries.Main_Router import Router


class HTTP_SERVER(http.server.BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        self._router = Router(self)
        http.server.BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def _set_headers(self, err_code=404, content_type='text/html', length=0, cors=False):
        self.send_response(err_code)

        self.send_header('Content-type', content_type)
        if cors:
            self.send_header('Access-Control-Allow-Origin', '*')

        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.headers['Content-Type'] == 'application/json':
            self.send_response(405)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
        else:
            input_data = self.read_data(False) # GET NO JSON
            self._router.route(path=self.path, data=input_data, json_rpc=False)

    def do_POST(self):

        if self.headers['Content-Type'] == 'application/json':
            input_data = self.read_data(True, True) # POST JSON
            self._router.route(path=self.path, data=input_data, json_rpc=True)
        else:
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
            if ctype == 'multipart/form-data':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('In development')
                
                
                '''input_data = {}
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                fields = cgi.parse_multipart(self.rfile, pdict)
                return_values_content = fields.get('input_file_script_return')
                input_data['return'] = return_values_content[0].decode("utf-8")

                file_content = fields.get('file_script')
                input_data['script'] = file_content[0].decode("utf-8")
                self._router.route(path=self.path, data=input_data, json_rpc=False)'''
                
                

            else:
                input_data = self.read_data() # POST NO JSON
                self._router.route(path=self.path, data=input_data, json_rpc=False)

    def read_data(self, is_POST=True, JSON = False):
        if is_POST:
            POSTDATA = {}
            if JSON:
                POSTDATA = self.rfile.read(int(self.headers['Content-Length'])).decode()
            else:
                if self.rfile:
                    for key, value in dict(urllib.parse.parse_qs(self.rfile.read(int(self.headers['Content-Length'])).decode())).items():
                        POSTDATA[key] = value[0]
            return POSTDATA
        else:
            if JSON:
                GETDATA = None
                if "?" in self.path:
                    GETDATA = urllib.parse.parse_qsl(self.path.split("?")[1], True)
            else:
                GETDATA = {}
                if "?" in self.path:
                    for key, value in dict(urllib.parse.parse_qsl(self.path.split("?")[1], True)).items():
                        GETDATA[str(key)] = str(value)
            return GETDATA


class ThreadedServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """lalala"""