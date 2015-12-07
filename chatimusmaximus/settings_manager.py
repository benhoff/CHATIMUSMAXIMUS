from os import path
from collections import OrderedDict
from operator import itemgetter
import yaml
from gui.models.settings_model import SettingsModel


class _OrderedLoader(yaml.Loader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def _construct_mapping(loader, node):
    loader.flatten_mapping(node)
    result = OrderedDict(sorted(loader.construct_pairs(node),
                                key=itemgetter(0)))

    return result


_OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                               _construct_mapping)


def _validate_settings_not_blank(setting):
    settings_have_values = False
    for key, value in setting.items():
        if value == str() or key == 'display_settings' or key == 'connect':
            pass
        else:
            settings_have_values = True
            break
    return settings_have_values


def _append_parent_attribute(data: OrderedDict):
    for child in data.values():
        if isinstance(child, OrderedDict):
            child.parent = data
            _append_parent_attribute(child)


class SpecialDict(OrderedDict):
    def __init__(self, *args, **kwargs):
        super().__init__(sorted(kwargs.items()))

    def __getitem__(self, index):
        if isinstance(index, tuple):
            item = self
            for key in index:
                if item != ():
                    item = item[key]
            return item
        else:
            return super().__getitem__(index)


class SettingsManager(object):
    def __init__(self):
        self.settings = None
        self._get_settings_helper()
        _append_parent_attribute(self.settings)
        self.settings_model = SettingsModel(self.settings)

    def _get_settings_helper(self):
        main_dir = path.dirname(path.realpath(__file__))
        default_filepath = path.join(main_dir, 'default_settings.yml')
        user_filepath = path.join(main_dir, 'settings.yml')

        # open the default file and get version information
        with open(default_filepath) as default_filestream:
            default_filesettings = yaml.load(default_filestream)

        current_version = default_filesettings['version'].split('.')

        if path.exists(user_filepath):
            filepath = user_filepath
        else:
            filepath = default_filepath

        with open(filepath) as setting_file:
            self.settings = yaml.load(setting_file, _OrderedLoader)

        self.settings = SpecialDict(**self.settings)

        # get the settings version out and split on the `.` operator
        settings_version = self.settings.pop('version').split('.')
        if (not settings_version[0] == current_version[0] or
                not settings_version[1] == current_version[1]):
            # TODO: add in logic to help user migrate changes
            print('Settings file changed, please update {}'.format(filepath))

    def register_plugin_manager(self, plugin_manager):
        # FIXME: Hack
        plugins = plugin_manager.website_plugins.get_plugins()
        for plugin in plugins:
            setting = self.settings[plugin.platform]
            has_values = _validate_settings_not_blank(setting)
            if (not has_values and
                    not setting['display_settings']['display_missing']):
                self.settings.pop(plugin.platform)
                break
            if has_values and setting['connect']:
                plugin.activate(setting)

        f = self.settings_model.instantiate_website
        f.connect(plugin_manager.activate_website)

        f = self.settings_model.manage_website_state
        f.connect(plugin_manager.change_website_state)

    def register_main_window(self, main_window):
        main_window.set_settings(self.settings)
        main_window.settings_model = self.settings_model
        f = self.settings_model.set_text_color_signal
        f.connect(main_window.set_color)

        f = self.settings_model.command_prompt_signal
        f.connect(main_window.set_command_prompt)
