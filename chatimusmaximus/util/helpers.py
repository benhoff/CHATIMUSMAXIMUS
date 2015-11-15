from os import path
import yaml
import websites

import pluginmanager


def _validate_settings_not_blank(setting):
    settings_have_values = False
    for key, value in setting.items():
        if value == str() or key == 'display_settings' or key == 'connect':
            pass
        else:
            settings_have_values = True
            break
    return settings_have_values


def instantiate_plugin_manager(settings):
    website_interface = pluginmanager.PluginInterface()
    website_interface.collect_plugins(websites)
    plugins = website_interface.get_instances()

    for plugin in plugins:
        setting = settings[plugin.platform]
        has_values = _validate_settings_not_blank(setting)

        # NOTE: HACK
        if (not has_values and
                not setting['display_settings']['display_missing']):

            # NOTE: plugin setting value is removed here
            settings.pop(plugin.platfrom)
            # log.info('Plugin {} not being used'.format(plugin_platform))
            break

        # check to see if  are registered in plugins
        if has_values and setting['connect']:
            plugin.activate(setting)

    return website_interface


def get_settings_helper():
    """
    This helper loads the information from the file
    and works with the versioning information in the settings
    """
    # get the main directory
    main_dir = path.realpath(path.join(path.dirname(__file__), '..'))
    # get our default filepath and perferred filepath names using main dir
    default_filename = path.join(main_dir, 'default_settings.yml')
    perferred_filename = path.join(main_dir, 'settings.yml')

    # open the default file and get version information
    with open(default_filename) as default_filestream:
        default_filesettings = yaml.load(default_filestream)

    # get the settings version out and split on the `.` operator
    default_version = default_filesettings['version'].split('.')

    # allow our user to put info in default_settings.yml or settings.yml
    if path.exists(perferred_filename):
        filename = perferred_filename
    else:
        filename = default_filename

    with open(filename) as setting_file:
        settings = yaml.load(setting_file)
    # get the settings version out and split on the `.` operator
    settings_version = settings.pop('version').split('.')
    if (not settings_version[0] == default_version[0] or
            not settings_version[1] == default_version[1]):
        # TODO: add in logic to help user migrate changes
        print('Settings file has changed, please update {}'.format(filename))
    return settings
