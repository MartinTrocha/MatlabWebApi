from libraries.Main_Controller import Main_Controller
from libraries.Api_manager import API_manager

import uuid
import time

class UsersController(Main_Controller):
    def __init__(self, server):
        Main_Controller.__init__(self, server)
        Main_Controller.db_connect(self)
        self.api = API_manager()

    '''
    register user by credentials, not need api_key
    '''
    def register_user(self, input_data):
        return 200, "tutoka"
        if not self.api.validate_user(input_data):
            return 400, self.api.error_msg

        __password, __salthash = self.api.hash_password(str(input_data['password']).strip(), str(input_data['email']).strip())
        sql = "INSERT INTO `users` (`email`, `password`, `salt`, `date_added`) VALUES ( '"+str(input_data['email']).strip()+"', '"+str(__password).strip()+"', '"+str(__salthash).strip()+"', '"+str(int(time.time()))+"' )"
        if self._db.exec_command(_sqlcommand=sql, _return=False, _multiple=False) is False:
            return 500, "DB ERROR"
        return 200, "Successfully registered"

    '''
    generate api_key or return if already exists
    '''
    def generate_api_key(self, input_data):
        user = self.api.validate_user_by_db(input_data)
        if not user:
            return 400, self.api.error_msg

        sql = " SELECT * FROM `api_key` WHERE `u_id` = '"+str(user['u_id'])+"' "
        result2 = self._db.exec_command(_sqlcommand=sql, _return=True, _multiple=False)

        if result2 is None: #DEVINFO GENERATE API KEY
            __api_key = uuid.uuid4()

            #DEVINFO create user storage space
            if not self.api.create_user_storage_space(str(__api_key)):
                return 500, "Internal error, cannot create user's storage space"

            sql = "INSERT INTO `api_key` (`u_id`, `api_key`, `date_added`) VALUES ( '"+str(user['u_id'])+"', '"+str(__api_key)+"', '"+str(int(time.time()))+"' )"
            result =  self._db.exec_command(_sqlcommand=sql, _return=False, _multiple=False)
            if result is False:
                return 500, "DB ERROR"

            return 200, str(__api_key)
        else: #DEVINFO RETURN EXISTING API KEY
            return 200, str(result2['api_key'])

    '''
    Remove api_key by user credentials
    '''
    def remove_api_key(self, input_data):
        user = self.api.validate_user_by_db(input_data)
        if not user:
            return 400, self.api.error_msg

        sql = "SELECT * FROM `api_key` WHERE `u_id` = '" + str(user['u_id']) + "' "
        result = self._db.exec_command(_sqlcommand=sql, _return=True, _multiple=False)

        if not self.api.remove_user_storage_space(str(result['api_key'])):
            return 500, "Internal Error, cannot remove user's storage space"

        sql = "DELETE FROM `api_key` WHERE `u_id` = '" + str(user['u_id']) + "' "
        self._db.exec_command(_sqlcommand=sql, _return=True, _multiple=False)
        return 200, "Successfully deleted api key"

    '''
    Remove user by his credentials
    '''
    def remove_user(self, input_data):
        user = self.api.validate_user_by_db(input_data)
        if not user:
            return 400, self.api.error_msg

        sql = "SELECT * FROM `api_key` WHERE `u_id` = '" + str(user['u_id']) + "' "
        result = self._db.exec_command(_sqlcommand=sql, _return=True, _multiple=False)

        if result is not None:
            if not self.api.remove_user_storage_space(str(result['api_key'])):
                return 500, "Internal Error, cannot remove user's storage space"

            sql = " DELETE FROM `api_key` WHERE `u_id` = '" + str(user['u_id']) + "' "
            self._db.exec_command(_sqlcommand=sql, _return=True, _multiple=False)

        sql = " DELETE FROM `users` WHERE `u_id` = '" + str(user['u_id']) + "' "
        self._db.exec_command(_sqlcommand=sql, _return=True, _multiple=False)
        return 200, "Successfully deleted user"