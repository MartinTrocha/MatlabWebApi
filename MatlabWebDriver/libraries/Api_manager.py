from libraries.Driver_DB import Driver_DB
from configs.app import CONFIG

import random
import os
import shutil
import hashlib
import time
import uuid

class API_manager(object):
    def __init__(self):
        self.error_msg = ""
        self.__ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self._db = Driver_DB()
        self._db.connect(_host='localhost', _user='root', _password='meglepetes', _db='matlab', _port=None)

    def validate_user(self, input_data):
        self.error_msg = "Success"
        if input_data['email'] is None or input_data['password'] is None:
            self.error_msg = "Invalid params"
            return False

        if not isinstance(input_data['email'], str) or not isinstance(input_data['password'], str):
            self.error_msg = "Invalid params format"
            return False

        if len(input_data['email']) < 8:
            self.error_msg = "Invalid email format"
            return False

        if len(input_data['password']) < 8:
            self.error_msg = "Password minimum length is 8 characters"
            return False
        return True

    def validate_user_by_db(self, input_data):
        if not self.validate_user(input_data):
            return False

        sql = "SELECT * FROM `users` WHERE `email` = '" + input_data['email'] + "'"
        result = self._db.exec_command(_sqlcommand=sql, _return=True, _multiple=False)
        if result is False:
            self.error_msg = "User not found"
            return False

        __password = result['salt'] + input_data['password'] + input_data['email']
        __password = str(hashlib.sha224(__password.encode()).hexdigest())

        if __password != result['password']:
            self.error_msg = "Invalid email or password"
            return False
        return result

    def validate_user_by_api_key(self, input_data):

        if input_data['api_key'] is None:
            self.error_msg = "Invalid API KEY"
            return False

        if not isinstance(input_data['api_key'], str):
            self.error_msg = "Invalid API KEY format"
            return False

        if len(input_data['api_key']) < 8:
            self.error_msg = "Invalid API KEY format"
            return False

        sql = "SELECT * FROM `api_key` WHERE `api_key` = '" + str(input_data['api_key']) + "'"
        result = self._db.exec_command(_sqlcommand=sql, _return=True, _multiple=False)
        if result is None:
            return False
        return True

    def generate_salt(self):
        __salt = []
        for i in range(16):
            __salt.append(random.choice(self.__ALPHABET))
        __salthash = "".join(__salt)
        return __salthash

    def hash_password(self, password, other):
        __salthash = self.generate_salt()
        __password = __salthash + password + other
        __password = str(hashlib.sha224(__password.encode()).hexdigest())
        return __password, __salthash

    def create_user_storage_space(self, apikey):
        if not isinstance(apikey, str):
            return False

        path = CONFIG['BASEPATH']+'storage/users_space/'+apikey
        if os.path.isdir(path):
            return True

        os.mkdir(path, mode=0o777)
        #athlib.Path(path).mkdir(mode=0o777, parents=True, exist_ok=True)
        if os.path.isdir(path):
            return True
        return False

    def remove_user_storage_space(self, apikey):
        if not isinstance(apikey, str):
            return False

        path = CONFIG['BASEPATH']+'storage/users_space/'+apikey
        if not os.path.isdir(path):
            return True

        shutil.rmtree(path)
        if not os.path.isdir(path):
            return True
        return False

    def check_users_storage_space(self, apikey):
        path = CONFIG['BASEPATH'] + 'storage/users_space/' + apikey
        if os.path.isdir(path):
            return True
        return False

    def add_file_db(self, user_id, filename, extension, api_key):

        path = CONFIG['BASEPATH'] + '/storage/users_space/' + api_key
        if not os.path.isdir(path):
            return False

        full_path = path + '/' + filename + extension
        if not os.path.isfile(full_path):
            return False

        sql = "INSERT INTO `user_files` (`u_id`, `path`, `filename`, `extension`, `date_added`, `date_last_used`) VALUES ( '"+str(user_id)+"', '"+str(path)+"', '"+str(filename)+"', '"+str(extension)+"', '"+str(time.time())+"', '"+str(time.time())+"')"
        self._db.exec_command(_sqlcommand=sql, _return=False, _multiple=False)
        return True

    def update_file_db_use(self, uf_id):
        sql = "UPDATE `user_file` SET `date_last_used` = '"+str(time.time())+"' WHERE `uf_id` = '"+uf_id+"' "
        self._db.exec_command(_sqlcommand=sql, _return=False, _multiple=False)
        return True

    def get_user_id_by_api_key(self, api_key):
        sql = "SELECT u_id FROM `api_key` WHERE `api_key` = '"+str(api_key)+"'"
        user_id = self._db.exec_command(_sqlcommand=sql, _return=True, _multiple=False)
        return user_id['u_id']