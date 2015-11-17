from os import path
import yaml
from .gui.models.settings_model import SettingsModel

class SettingsManager(object):
    def __init__(self):
        self.settings = None
        self._get_settings_helper()
        self.settings_model = SettingsModel(self.settings)

    def _get_settings_helper(self):
        main_dir = path.dirname(path.realpath(__file__))
        default_filepath = path.join(main_dir, 'default_settings.yml')
        user_filepath = path.join(main_dir, 'settings.yml')

        # open the default file and get version information
        with open(default_filename) as default_filestream:
            default_filesettings = yaml.load(default_filestream)

        current_version = default_filesettings['version'].split('.')

        if path.exists(user_filepath):
            filepath = user_filepath 
        else:
            filepath = default_filepath 

        with open(filepath) as setting_file:
            self.settings = yaml.load(setting_file)

        # get the settings version out and split on the `.` operator
        settings_version = settings.pop('version').split('.')
        if (not settings_version[0] == default_version[0] or
                not settings_version[1] == default_version[1]):
            # TODO: add in logic to help user migrate changes
            print('Settings file has changed, please update {}'.format(filename))

    def register_plugin_manager(self, plugin_manager):
        self.settings_model.instantiate_website.connect(plugin_manager.activate_website)
        self.settings_model.manage_website_state.connect(plugin_manager.change_website_state)

    def register_main_window(self, main_window):
        main_window.set_settings(self.settings_model)
        self.settings_model.set_text_color_signal.connect(main_window.set_color)
        self.settings_model.command_prompt_signal.connect(main_window.set_command_prompt)
