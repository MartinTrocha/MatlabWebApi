from libraries.Driver_DB import Driver_DB

class Main_Controller(object):

    def __init__(self, server):
        self._server = server
        self._db = Driver_DB()

    @property
    def server(self):
        return self._server

    @property
    def db(self):
        return self._db

    def db_connect(self):
        self._db.connect(_host='localhost', _user='root', _password='meglepetes', _db='matlab', _port=None)