from os import path
import json
import socket_protocols

default_filename = 'default_settings.json'
perferred_filename = 'settings.json'

if path.exists(perferred_filename):
    filename = perferred_filename
else:
    filename = default_filename
    print('Change your default settings!')

with open(filename) as setting_file:    
    settings = json.load(setting_file)

chrome_server_settings = settings['chrome_tcp_server']
youtube_socket = socket_protocols.ReadOnlyTCPSocket(chrome_server_settings['host'],
                                                    chrome_server_settings['port'])

wpc_settings = settings['watchpeoplecode']
wpc_socket = socket_protocols.ReadOnlyWebSocket(wpc_settings['channel'])

twitch_settings = settings['twitch']
irc_client = socket_protocols.ReadOnlyIRCBot(twitch_settings['channel'], 
                                             twitch_settings['nick'], 
                                             twitch_settings['oauth_token'])
