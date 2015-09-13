import os
import yaml
import logging

from websites import WebsitePlugin
import simpleyapsy
import plugins

def validate_settings_not_blank(setting):
    settings_have_values = False
    for key, value in setting.items():
        if value == str() or key == 'display_settings' or key == 'connect':
            pass
        else:
            settings_have_values = True
            break
    return settings_have_values

def instantiate_plugin_manager(settings):
    file_dir = os.path.dirname(os.path.realpath(__file__))
    website_path = os.path.join(file_dir, 'websites')

    plugin_manager = simpleyapsy.PluginManager({'website':WebsitePlugin, 
                                                'listener':plugins.ListenerPlugin}, 
                                               [plugins.__path__[0], website_path])

    plugin_manager.collectPlugins()

    for website_plugin_info in plugin_manager.getPluginsOfCategory('website'):
        website_setting = settings[website_plugin_info.name]
        has_values = validate_settings_not_blank(website_setting)
    
        # NOTE: HACK
        if not has_values and not setting['display_settings']['display_missing']:
            removed_plugin = settings.pop(settings_key)
            log.info('Plugin {} not being used'.format(removed_plugin))
            break

        # check to see if  are registered in plugins
        if has_values and setting['connect']:
            website_plugin_info.plugin_object.activate(setting)

    return plugin_manager

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

