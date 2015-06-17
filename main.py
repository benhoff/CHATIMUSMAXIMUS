import sys 
from os import path
import json
from PyQt5 import QtWidgets, QtNetwork, QtCore
from gui import MainWindow
import socket_protocols


# handle the settings
default_filename = 'default_settings.json'
perferred_filename = 'settings.json'

if path.exists(perferred_filename):
    filename = perferred_filename
else:
    filename = default_filename
    print('Change your default settings!')

with open(filename) as setting_file:    
    settings = json.load(setting_file)

# alias out the individual settings for each of the sockets
chrome_server_settings = settings['chrome_tcp_server']
wpc_settings = settings['watchpeoplecode']
twitch_settings = settings['twitch']

# instantiate the sockets
wpc_socket = socket_protocols.ReadOnlyWebSocket(wpc_settings['channel'])
youtube_socket = socket_protocols.ReadOnlyTCPSocket(chrome_server_settings['host'],
                                                    chrome_server_settings['port'])

irc_client = socket_protocols.ReadOnlyIRCBot(twitch_settings['channel'], 
                                             twitch_settings['nick'], 
                                             twitch_settings['oauth_token'])

# create the GUI
app = QtWidgets.QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
# connect the sockets signals to the GUI
youtube_socket.chat_signal.connect(main_window.chat_slot)
wpc_socket.chat_signal.connect(main_window.chat_slot)
irc_client.chat_signal.connect(main_window.chat_slot)
# loop... forever
sys.exit(app.exec_())
