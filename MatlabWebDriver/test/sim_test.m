
load_system('sldemo_bounce')

tmp = find_system('sldemo_bounce', 'Type', 'Block')
acc_port_handle = get_param(tmp(6), 'PortHandles')

new_block = add_block('simulink/Sinks/To Workspace','sldemo_bounce/Position', 'VariableName', 'Variable_Position', 'SaveFormat', 'Array')
new_block_port_handle = get_param(new_block, 'PortHandles')
set_param('sldemo_bounce/Position', 'position', [600,240,650,270]);
add_line('sldemo_bounce', acc_port_handle{1}.Outport(1), new_block_port_handle.Inport(1));
save_system('sldemo_bounce')


set_param('sldemo_bounce','SimulationCommand','Start', 'SimulationCommand','Pause')
set_param('sldemo_bounce','SimulationCommand','Continue', 'SimulationCommand','Pause')
set_param('sldemo_bounce','SimulationCommand','Continue', 'SimulationCommand','Pause')
set_param('sldemo_bounce','SimulationCommand','Continue', 'SimulationCommand','Pause')
set_param('sldemo_bounce','SimulationCommand','Continue', 'SimulationCommand','Pause')
set_param('sldemo_bounce','SimulationCommand','Continue', 'SimulationCommand','Pause')
set_param('sldemo_bounce','SimulationCommand','Continue', 'SimulationCommand','Pause')
set_param('sldemo_bounce','SimulationCommand','Continue', 'SimulationCommand','Pause')
set_param('sldemo_bounce','SimulationCommand','Continue', 'SimulationCommand','Pause')
set_param('sldemo_bounce','SimulationCommand','Stop')

close_system('sldemo_bounce')