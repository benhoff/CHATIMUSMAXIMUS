import irc3
from irc3.plugins.command import command

@irc3.plugin
class EchoToMessage(QtCore.QObject):
    chat_signal = QtCore.pyqtSignal(str, str, int)

    def __init__(self, bot):
        self.bot = bot

    @command(permission='view')
    def echo(self, mask, target, args):
        self.chat_signal.emit(mask.nick, ' '.join(args['<words>']), gui.StatusBarSelector.Twitch.value)
