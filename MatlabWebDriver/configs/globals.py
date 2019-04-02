matlab_engine_instances = []
matlab_engine_instances_indexes = []
instances_in_use = []

'''
    Returns free matlab instance
'''
def get_free_instance():
    ret_val = list(set(matlab_engine_instances) - set(instances_in_use))
    if len(ret_val) > 0:
        return ret_val[0]
    return None