# Socket protocols

Socket protocols implement an IRC protocol, a websocket protocl, and a TCP protocol in the form of ReadOnlyIRCBot, ReadOnlyWebSocket, and ReadOnlyTCPSocket, respectively.

As the names would imply, each class is a very narrowly implemented, brittle concrete class.

# ReadOnlyWebSocket
Written to interface with the WatchPeopleCode socket.io chat server

# ReadOnlyIRCBot
Written to interface with Twitch's IRC chat

# ReadOnlyTCPSocket
Written to interface with the chrome extension in this library

# TODO:
Implement automatic retrying logic and error handeling (even as simple as printing to console)
Test/Fix ReadOnlyTCPSocket
