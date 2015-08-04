import os 

class IPluginRegistry(type):
    plugins = []
    def __init__(cls, name, bases, attrs):
        if name != 'IPlugin':
            IPluginRegistry.plugins.append(cls)

for filename in os.listdir(os.path.dirname(__file__)):
    modname, ext  = os.path.splittext(filename)
    if ext == '.py' and modname != 'base_plugin':
        file_, path, descr = imp.find_module(modname, [dir])
        if file_:
            mod = imp.load_module(modname, file_, path, descr)
