from libraries.Driver_Main import Driver_Main
from configs import globals
import matlab.engine


class InstanceDriver(Driver_Main):

    def __init__(self):
        Driver_Main.__init__(self)

        self.CONST_TAG = "[InstanceDriver]"

        self.num_of_instances = 1


        Driver_Main.log(self, "Instance Driver Initialized", tag=self.CONST_TAG, type='info')


    '''
        Create default num of matlab instances 
    '''
    def create_default_matlab_instances(self):
        for x in range(self.num_of_instances):
            globals.matlab_engine_instances.insert(x, matlab.engine.start_matlab("-nodisplay -r matlab.engine.shareEngine"))
            globals.matlab_engine_instances_indexes.append(x)

        Driver_Main.log(self, "Created "+str(self.num_of_instances)+" default matlab instances", tag=self.CONST_TAG, type='info')


    '''
        Returns arrays of matlab instances
    '''
    def get_matlab_instances(self):
        Driver_Main.log(self, "Request for matlab instances", tag=self.CONST_TAG, type='info')
        return globals.matlab_engine_instances


    '''
        Creates additional matlab instance
        If success then returns new matlab instance otherwise None
    '''
    def create_new_matlab_instance(self):
        index = len(globals.matlab_engine_instances) + 1

        globals.matlab_engine_instances.insert(index, matlab.engine.start_matlab('-nodisplay -r matlab.engine.shareEngine'))
        globals.matlab_engine_instances_indexes.append(index)
        Driver_Main.log(self, "Request for new matlab instance", tag=self.CONST_TAG, type='info')

        if globals.matlab_engine_instances[index] is not None:
            Driver_Main.log(self, "Request for new matlab instance successfull", tag=self.CONST_TAG, type='success')
            return globals.matlab_engine_instances[index]

        Driver_Main.log(self, "Request for new matlab instance failed", tag=self.CONST_TAG, type='error')
        return None


