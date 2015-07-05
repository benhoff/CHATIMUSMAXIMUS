import sys 
import os
import json
from PyQt5 import QtWidgets, QtNetwork, QtCore
import sleekxmpp
from gui import MainWindow
import socket_protocols

from youtube import YoutubeScrapper
import utils
from xmpp_client import ReadOnlyXMPPBot

def get_settings_helper():
    default_filename = 'default_settings.json'
    perferred_filename = 'settings.json'

    if os.path.exists(perferred_filename):
        filename = perferred_filename
    else:
        filename = default_filename

    with open(filename) as setting_file:    
        settings = json.load(setting_file)

    app_settings = settings['app_settings']
    if app_settings['warn_user_about_settings']: 
        utils.settings_warner(settings)

    return settings

def instantiate_chats_helper(settings):
    """
    returns a list of all instantiated chats
    """
    # create the list to return
    chat_site_list = []

    # alias out the individual settings for each of the sockets
    wpc_settings = settings['watchpeoplecode']
    twitch_settings = settings['twitch']
    livecode_settings = settings['livecode']
    youtube_settings = settings['youtube']
    
    # check to see if there's a channel associated with WatchPeopleCode website
    if wpc_settings['channel'] is not str():
        # instanatiate websocket to WatchPeopleCode based on the passed in channel
        wpc_socket = socket_protocols.ReadOnlyWebSocket(wpc_settings['channel'])
        # append instantiated websocket to chat list
        chat_site_list.append(wpc_socket)
    
    # check to see if user has passed in both the channel and the 
    # OAuth token in order to instantiate the twitch client
    if twitch_settings['channel'] != str() and \
            (twitch_settings['oauth_token'] != str() or \
             os.getenv('TWITCH_KEY')):
        
        # create the irc client
        irc_client = socket_protocols.ReadOnlyIRCBot(twitch_settings['channel'], 
                                                     twitch_settings['nick'], 
                                                     twitch_settings['oauth_token'])
   
        # append instantiated irc client to chat list
        chat_site_list.append(irc_client)
    
    # check for youtube video url, and create youtube scrapper if present
    if youtube_settings['video_url'] != str() or os.getenv('YOUTUBE_URL'):
        youtube_scrapper = YoutubeScrapper(youtube_settings['video_url'])
        # append instantiated yotuube scraper to chat list
        chat_site_list.append(youtube_scrapper)
    
    # check for livecode channel and password
    if livecode_settings['name'] != str() and (livecode_settings['pass'] != str() or os.getenv('LIVECODE_PASS')):
        # check to see the user has passed in a bot nick and assign it if so
        if livecode_settings['bot_nick'] != str():
            bot_nick = livecode_settings['bot_nick']
        else:
            bot_nick = 'ReadOnlyBot'

        jid = sleekxmpp.JID(local=livecode_settings['name'], 
                            domain='livecoding.tv', 
                            resource='CHATIMUSMAXIMUS')

        livecode = ReadOnlyXMPPBot(jid, livecode_pass, nick=bot_nick)
        livecode.connect()
        livecode.process()
        chat_site_list.append(livecode)

    return chat_site_list

settings = get_settings_helper()
chat_list = instantiate_chats_helper(settings)
# create the GUI
app = QtWidgets.QApplication(sys.argv)
main_window = MainWindow()
main_window.show()

# connect the sockets signals to the GUI
for chat in chat_list:
    chat.chat_signal.connect(main_window.chat_string_slot)

# loop... forever
sys.exit(app.exec_())
