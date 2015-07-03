def _wpc_validations(json_object):
    try:
        wpc_settings = json_object['watchpeoplecode']
        if wpc_settings['channel'] == str():
            print('No WatchPeopleCode channel name given in settings!')
    # TODO: add in some print logic here!
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

def validate_json_settings(json_object):
    _wpc_validations(json_object)
    _twitch_validation(json_object)
