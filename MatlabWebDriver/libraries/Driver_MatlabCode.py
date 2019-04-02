from libraries.Driver_Main import Driver_Main
from libraries.Api_manager import API_manager
from configs.app import CONFIG
import os
import time
import uuid

class MatlabCode(Driver_Main):

    def __init__(self):
        Driver_Main.__init__(self)

        self.CONST_TAG = "[MatlabCodeDriver]"
        self.api = API_manager()

        self.script = ""
        self.script_file = ""
        self.workspace_return = []
        self.error_msg = ""
        self.return_values = {}
        self.script_file_name = ""
        Driver_Main.log(self, "Matlab Code Driver Initialized", self.CONST_TAG, 'info')

    #TODO subory sa hned nemazu ale daju sa do DB a obmedzi sa pocet
    #TODO listovanie suborov aby sa dalo vratit aj spat
    def run_script(self, engine, data):
        if not self.prepare(data=data):
            return False

        path = CONFIG['BASEPATH']+'/storage/users_space/'+data['api_key']
        engine.cd(path)
        engine.cd(path)# Pre istotu
        engine.run(self.script_file_name, nargout=0)

        if self.workspace_return == '*':
            self.workspace_return = engine.who('*')

        for r in self.workspace_return:
            self.return_values[r] = str(engine.workspace[r])

        engine.clear(nargout=0)

        os.remove(self.script_file)
        return str(self.return_values)

    def prepare(self, data):
        self.script = ""
        self.script_file = ""
        self.workspace_return = []
        self.return_values = {}

        if not self.valid_data(_data=data):
            return False

        if not self.save_script_file(data=data):
            return False

        if not self.parse_return_values(data=data):
            return False
        return True

    def parse_return_values(self, data):
        for d in str(data['return']).split(','):
            d = d.strip()
            if isinstance(d, str) and len(d) > 0:
                self.workspace_return.append(d)

        if '*' in self.workspace_return:
            self.workspace_return = "*"

        if self.workspace_return.__len__() == 0:
            self.error_msg = "Parse error! Return values empty"
            return False
        return True

    def save_script_file(self, data):
        path = CONFIG['BASEPATH']+'storage/users_space/'+str(data['api_key'])

        if not os.path.isdir(path):
            return False

        file_name, extension = self.parse_file_name()
        if 'file_name' in data:
            file_name, extension = self.parse_file_name(file_name=data['file_name'], matlab=True)
        path = path+'/'+file_name+extension

        try:
            f = open(path, 'w')
            f.writelines(str(data['script']))
            f.close()

            self.script_file_name = file_name+extension
            self.script_file = path
            user_id = self.api.get_user_id_by_api_key(data['api_key'])
            if user_id:
                return self.api.add_file_db(user_id=user_id, filename=file_name, extension=extension, api_key=str(data['api_key']))
            return False
        except FileExistsError as e:
            self.error_msg = "Local file could not be created"
            return False

    def valid_data(self, _data):
        if _data is None:
            self.error_msg = "Input data not set"
            return False

        if _data['script'] is None:
            self.error_msg = "Input script not set"
            return False

        if _data['return'] is None:
            self.error_msg = "Return values not set"
            return False

        if _data['api_key'] is None:
            self.error_msg = "API KEY not set"
            return False

        if not isinstance(_data['script'], str):
            self.error_msg = "Input script is not string"
            return False

        if not isinstance(_data['return'], str):
            self.error_msg = "Return values bad format"
            return False

        if not isinstance(_data['api_key'], str):
            self.error_msg = "API KEY bad format"
            return False

        if len(_data['script']) < 1:
            self.error_msg = "Input script empty"
            return False

        if len(_data['return']) < 1:
            self.error_msg = "Return values empty"
            return False

        if len(_data['api_key']) < 1:
            self.error_msg = "Return values empty"
            return False
        return True

    def parse_file_name(self, file_name = None, matlab = True):
        if file_name is not None:
            if isinstance(file_name, str):
                tmp = file_name.split('.')
                if tmp.__len__() == 2:
                    return tmp[0], tmp[1]
        if matlab:
            return 'matlab_'+str(int(time.time())), '.m'
        return 'simulink_' + str(int(time.time())), '.slx'
















































        '''func = matlab.engine.matlabengine.MatlabFunc(engine, _function)
        future = func.__call__(_input, async=_async)

        if _async:
            self.logger.log('asyncccc2c is done ' + str(future.done()), self.CONST_TAG, 'info')
            return future.result()
        else:
            return future'''


    '''def simulink(self, engine, step_by_step = False):
        #engine.cd('/home/martin/Documents/MATLAB/Examples/simulink_general/sldemo_bounceExample')
        engine.cd('/home/martin/MatlabWebDriver/')
        if step_by_step:
            #engine.sim('sldemo_bounce')
            engine.sim_test(nargout=0)
            result = engine.workspace['Variable_Position']
            return result
        else:
            result = engine.sim('sldemo_bounce_two_integrators')
            return result

    def simulink2(self, engine):
        engine.cd('/home/martin/MatlabWebDriver/')

        engine.load_system('sldemo_bounce')

        #tmp = engine.find_system('sldemo_bounce', 'Type', 'Block')
        #acc_port_handle = engine.get_param(tmp(6), 'PortHandles')

        #new_block = engine.add_block('simulink/Sinks/To Workspace', 'sldemo_bounce/Position', 'VariableName',
                              'Variable_Position', 'SaveFormat', 'Array')
        #new_block_port_handle = engine.get_param(new_block, 'PortHandles')
        #engine.sim('sldemo_bounce/Position', 'position', [600, 240, 650, 270]);
        #engine.add_line('sldemo_bounce', acc_port_handle{1}.Outport(1), new_block_port_handle.Inport(1));
        #engine.save_system('sldemo_bounce')

        engine.set_param('sldemo_bounce', 'SimulationCommand', 'Start', 'SimulationCommand', 'Pause', nargout=0)
        engine.set_param('sldemo_bounce', 'SimulationCommand', 'Continue', 'SimulationCommand', 'Pause', nargout=0)
        engine.set_param('sldemo_bounce', 'SimulationCommand', 'Continue', 'SimulationCommand', 'Pause', nargout=0)
        engine.set_param('sldemo_bounce', 'SimulationCommand', 'Continue', 'SimulationCommand', 'Pause', nargout=0)
        engine.set_param('sldemo_bounce', 'SimulationCommand', 'Continue', 'SimulationCommand', 'Pause', nargout=0)
        engine.set_param('sldemo_bounce', 'SimulationCommand', 'Continue', 'SimulationCommand', 'Pause', nargout=0)
        engine.set_param('sldemo_bounce', 'SimulationCommand', 'Continue', 'SimulationCommand', 'Pause', nargout=0)
        engine.set_param('sldemo_bounce', 'SimulationCommand', 'Continue', 'SimulationCommand', 'Pause', nargout=0)
        engine.set_param('sldemo_bounce', 'SimulationCommand', 'Continue', 'SimulationCommand', 'Pause', nargout=0)
        engine.set_param('sldemo_bounce', 'SimulationCommand', 'Stop')

        engine.close_system('sldemo_bounce')'''