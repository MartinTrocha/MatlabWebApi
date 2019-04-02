from libraries.Main_Controller import Main_Controller
from libraries.Driver_MatlabCode import MatlabCode
from libraries.Api_manager import API_manager
from configs import globals

class MatlabController(Main_Controller):

    def __init__(self, server):
        Main_Controller.__init__(self, server)
        self.api = API_manager()
        self.matlab = MatlabCode()

    def script_action(self, input_data = None):
        if self.api.validate_user_by_api_key(input_data) is False:
            return 400, self.api.error_msg

        _mi = globals.get_free_instance()
        result = self.matlab.run_script(_mi, data=input_data)

        if result is False:
            return 400, str(self.matlab.error_msg)
        return 200, str(result)

    def file_script_action(self, input_data = None):
        if self.api.validate_user_by_api_key(input_data):
            return 400, self.api.error_msg

        _mi = globals.get_free_instance()
        result = self.matlab.run_script(_mi, data=input_data)

        return 200, result