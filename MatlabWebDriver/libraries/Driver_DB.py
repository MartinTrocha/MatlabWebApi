import pymysql
import pymysql.cursors
pymysql.install_as_MySQLdb()

class Driver_DB(object):
    def __init__(self, ):
        self.__connector = None

    def connect(self, _host, _user, _password, _db, _port):
        self.__connector = pymysql.connect(host = _host, user = _user, password = _password, db = _db, port = _port, charset='utf8mb4', cursorclass = pymysql.cursors.DictCursor)

    def exec_command(self, _sqlcommand, _return = True, _multiple = False):
        result = None
        try:
            with self.__connector.cursor() as cursor:
                cursor.execute(_sqlcommand)
            self.__connector.commit()

            if _return and not _multiple:
                result = cursor.fetchone()
            if _return and _multiple:
                result = cursor.fetchall()
        finally:
            return result

    def disconnect(self):
        self.__connector.close()


