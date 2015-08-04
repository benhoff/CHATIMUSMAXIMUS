import os
import yaml

import sleekxmpp
import gui
import socket_protocols

from youtube import YoutubeScrapper
import utils
from xmpp_client import ReadOnlyXMPPBot
import sleekxmpp

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
    def set_status_helper(status_index):
        """
        inner loop helper
        """
        if main_window:
            main_window.set_service_icon(status_index, 
                                         True)

    # create the list to return
    chat_site_list = []
    if 'watchpeoplecode' in settings:
        wpc_settings = settings['watchpeoplecode']
        # check to see if there's a channel associated with 
        # WatchPeopleCode website
        if wpc_settings['channel'] is not str():
            # instanatiate websocket to WatchPeopleCode 
            # based on the passed in channel
            wpc_socket = socket_protocols.ReadOnlyWebSocket(
                    wpc_settings['channel'])

            # append instantiated websocket to chat list
            chat_site_list.append(wpc_socket)
            set_status_helper(gui.StatusBarSelector.WatchPeopleCode.value)
    if 'twitch' in settings:
        twitch_settings = settings['twitch']
        # check to see if user has passed in both the channel and the 
        # OAuth token in order to instantiate the twitch client
        if twitch_settings['channel'] != str() and \
                (twitch_settings['oauth_token'] != str() or \
                 os.getenv('TWITCH_KEY')):
            
            # create the irc client
            irc_client = socket_protocols.create_irc_bot(
                    twitch_settings['nick'],                                     
                    twitch_settings['oauth_token'],
                    channel=twitch_settings['channel'])

            irc_client.create_connection()
            irc_client.add_signal_handlers()
            irc_chat_plugin = irc_client.get_plugin(
                    socket_protocols.EchoToMessage)

            # append instantiated irc client to chat list
            chat_site_list.append(irc_chat_plugin)
            set_status_helper(gui.StatusBarSelector.Twitch.value)
    if 'livecoding' in settings:
        livecode_settings = settings['livecoding']
        # check for livecode channel and password
        if livecode_settings['name'] != str() and (livecode_settings['pass'] != str() or os.getenv('LIVECODE_PASS')):
            # check to see the user has passed in a bot nick and assign it if so
            bot_nick = livecode_settings['bot_nick'] if livecode_settings['bot_nick'] != str() else 'ReadOnlyBot'
            livecode_pass = livecode_settings['pass'] if livecode_settings['pass'] != str() else os.getenv('LIVECODE_PASS') 

            jid = sleekxmpp.JID(local=livecode_settings['name'], 
                                domain='livecoding.tv', 
                                resource='CHATIMUSMAXIMUS')

            livecode = ReadOnlyXMPPBot(jid, livecode_pass, nick=bot_nick)
            livecode.connect()
            livecode.process()
            chat_site_list.append(livecode)
            set_status_helper(gui.StatusBarSelector.Livecoding.value)
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
