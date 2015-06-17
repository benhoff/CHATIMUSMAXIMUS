from os import path
default_filename = 'default_settings.json'
perferred_filename = 'settings.json'

if path.exists(perferred_filename):
    filename = perferred_filename
else:
    filename = default_filename
    print('Change your default settings!')

settings_file = open(flename, 'r') 
read_all = settings_file.readlines()
# TODO: add in sweet JSON parsing
