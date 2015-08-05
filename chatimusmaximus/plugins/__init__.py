import os 
import imp
from plugins.base_plugin import IPluginRegistry, IPlugin


directory = os.path.dirname(os.path.realpath(__file__))
for filename in os.listdir(directory):
    # TODO: Figure out cleaner way to do this
    filename = os.path.join(directory, filename)
    print(filename)
    modname, ext  = os.path.splitext(filename)
    if ext == '.py' and modname != 'base_plugin' and modname != '__init__':
        file_, path, descr = imp.find_module(modname, [dir])
        if file_:
            mod = imp.load_module(modname, file_, path, descr)
