import os

import pluginmanager


def validate_settings_not_blank(setting):
    settings_have_values = False
    for key, value in setting.items():
        if value == str() or key == 'display_settings' or key == 'connect':
            pass
        else:
            settings_have_values = True
            break
    return settings_have_values
