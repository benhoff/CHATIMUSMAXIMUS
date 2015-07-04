import sys 
import os
import json
from PyQt5 import QtWidgets, QtNetwork, QtCore
from gui import MainWindow
import socket_protocols

from youtube import YoutubeScrapper
import utils

# handle the settings
default_filename = 'default_settings.json'
perferred_filename = 'settings.json'

if os.path.exists(perferred_filename):
    filename = perferred_filename
else:
    filename = default_filename

with open(filename) as setting_file:    
    settings = json.load(setting_file)

utils.validate_json_settings(settings)

# alias out the individual settings for each of the sockets
wpc_settings = settings['watchpeoplecode']
twitch_settings = settings['twitch']

# instantiate the sockets
wpc_socket = socket_protocols.ReadOnlyWebSocket(wpc_settings['channel'])
irc_client = socket_protocols.ReadOnlyIRCBot(twitch_settings['channel'], 
                                             twitch_settings['nick'], 
                                             twitch_settings['oauth_token'])

youtube_url = os.getenv('YOUTUBE_URL')

if youtube_url == str():
    print('No Youtube Scraper')

youtube_scrapper = YoutubeScrapper(youtube_url)

# create the GUI
app = QtWidgets.QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
# connect the sockets signals to the GUI
youtube_scrapper.chat_signal.connect(main_window.chat_string_slot)
wpc_socket.chat_signal.connect(main_window.chat_string_slot)
irc_client.chat_signal.connect(main_window.chat_string_slot)

# loop... forever
sys.exit(app.exec_())
