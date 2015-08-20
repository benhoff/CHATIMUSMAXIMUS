import os
import yaml

import plugins

def get_settings_helper():
    """
    This helper loads the information from the file
    and works with the versioning information in the settings
    """
    # get the main directory
    main_dir = os.path.dirname(os.path.realpath(__file__))
    # get our default filepath and perferred filepath names using main dir
    default_filename = os.path.join(main_dir, 'default_settings.yml')
    perferred_filename = os.path.join(main_dir, 'settings.yml')
    
    # open the default file and get version information
    with open(default_filename) as default_filestream:
        default_filesettings = yaml.load(default_filestream)

    # get the settings version out and split on the `.` operator
    default_version = default_filesettings['version'].split('.')
    
    # allow our user to put info in default_settings.yml or settings.yml
    if os.path.exists(perferred_filename):
        filename = perferred_filename
    else:
        filename = default_filename

    with open(filename) as setting_file:    
        settings = yaml.load(setting_file)
    # get the settings version out and split on the `.` operator
    settings_version = settings.pop('version').split('.')
    if not settings_version[0] == default_version[0] or not settings_version[1] == default_version[1]: 
        # TODO: add in logic to help user migrate changes
        print('Settings file has changed, please update {}'.format(filename))
    return settings

def instantiate_chats_helper(settings):
    """
    This helper parses through the settings and 
    and instantiates all of the used chats
    """
    # create the list to return
    chat_site_list = []
    plugins.get_plugins()
    # parse the plugins to just get the names
    str_plugins = [str(s).split('.')[0].split('/')[-1] for s in plugins.IPluginRegistry.plugins]

    # now check the settings keys and if any keys are found
    # that match the plugins, instantiate the plugin
    for settings_key in settings.keys():
        # check to see if  are registered in plugins
        if settings_key in str_plugins:
            # find the index
            index = str_plugins.index(settings_key)
            # grab the class instance
            kls = plugins.IPluginRegistry.plugins[index]
            # settings is a dict, so pass the key back in to get the settings
            instantiate_plugin = kls(settings[settings_key])
            # lastly, push the instantiated plugin onto list
            chat_site_list.append(instantiate_plugin)

    return chat_site_list
