ROUTES = [
    { 'expression' : r'^/$', 'controller' : 'controllers.MatlabController', 'action' : 'indexAction' },
    { 'expression' : r'^(/matlab|/matlab\?.)', 'controller' : 'controllers.MatlabController', 'action' : 'script_action' },
    { 'expression' : r'^(/matlab-file|/matlab-file/)', 'controller' : 'controllers.MatlabController', 'action' : 'file_script_action' },

    { 'expression' : r'^(/api-register|/api-register\?.)', 'controller' : 'controllers.UsersController', 'action' : 'register_user' },
    { 'expression' : r'^(/api-generate|/api-generate\?.)', 'controller' : 'controllers.UsersController', 'action' : 'generate_api_key' },
    { 'expression' : r'^(/api-remove|/api-remove\?.)', 'controller' : 'controllers.UsersController', 'action' : 'remove_api_key' },
    { 'expression' : r'^(/api-user-remove|/api-user-remove\?.)', 'controller' : 'controllers.UsersController', 'action' : 'remove_user' },
]