import os
import yaml

import sleekxmpp

import gui
import utils
import plugins

def fake_verify(*args):
    return

# monkey patch to fix issues with either livecode or 
# sleekxmpp. hard to tell where the problem is
sleekxmpp.xmlstream.cert.verify = fake_verify

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

def instantiate_chats_helper(settings, main_window=None, event_loop=None):
    """
    This helper parses through the settings and 
    and instantiates all of the used chats
    """
    # create the list to return
    chat_site_list = []
    for chat_site in settings.keys:
        if chat_site in IPluginRegistry.plugins:
            #chat_site_list.append(plugin(settings))
            pass

    if 'youtube' in settings:
        youtube_settings = settings['youtube']
        # check for youtube video url, and create youtube scrapper if present
        if youtube_settings['channel_id'] != str():
            youtube_url = 'http://www.youtube.com/channel/{}/live'.format(youtube_settings['channel_id'])
            youtube_scrapper = YoutubeScrapper(youtube_url)
            # append instantiated yotuube scraper to chat list
            chat_site_list.append(youtube_scrapper)
            set_status_helper(gui.StatusBarSelector.Youtube.value)
    

    return chat_site_list
