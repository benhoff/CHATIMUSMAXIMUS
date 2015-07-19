def _wpc_validations(json_object):
    try:
        wpc_settings = json_object['watchpeoplecode']
        if wpc_settings['channel'] == str():
            print('No WatchPeopleCode channel name given in settings!')
    except Exception as e:
        print(e)

def _twitch_validation(json_object):
    try:
        twitch_settings = json_object['twitch']
        if twitch_settings['oauth_token'] == str():
            print('No twitch OAUTH token!')
        if twitch_settings['channel'] == str():
            print('No channel specified for twitch!')
        if twitch_settings['nick'] == str():
            print('No nick specificed for twitch!')
    except Exception as e:
        print(e)

def _livecode_validations(json_object):
    try:
        livecode_settings = json_object['livecode']
        if livecode_settings['pass'] == str():
            print('No livecode password!')
    except Exception as e:
        print(e)

def _youtube_validation(json_object):
    try:
        youtube_settings = json_object['youtube']
        if youtube_settings['channel_id'] == str():
            print('No Youtube channel id given!')

    except Exception as e:
        print(e)


def settings_warner(json_object):
    """
    Provides feedback about the state of the settings
    file by printing to console
    """
    _wpc_validations(json_object)
    _twitch_validation(json_object)
    _livecode_validations(json_object)
    _youtube_validation(json_object)
