# CHATIMUSMAXIMUS GUI
currently sparsely implemented as a `QTextEdit`. The primary interface uses Qt's signal/slot mechanism, specially the slot named `chat_signal`.
`chat_signal` has been overloaded to accept either three strings (sender, message, platform) or a QByteArray and a platform string. 


# TODO:
automove cursor as chat appends
