import asyncio
import sqlite3
from PyQt5 import QtCore
# import auth here

class Database(object):
    VERSION = 1

    def update_schema(self, cursor):
        version = cursor.execute("PRAGMA user_version")
        if version.fetchone()[0] == 0:
            self.version_1(cursor)

    def version_1(self, cursor: sqlite3.Cursor):
        yt_table = 'CREATE TABLE youtube (youtubeid PRIMARY KEY ASC, FOREIGN KEY(userid) REFERENCES user(userid))'
        wpc_table = 'CREATE TABLE watchpeoplecode (watchpeoplecodeid PRIMARY KEY ASC, FOREIGN KEY(userid) REFERENCES user(userid))'
        livecode_table = 'CREATE TABLE livecoding (livecodingid PRIMARY KEY ASC, FOREIGN KEY(userid) REFERENCES user(userid))'
        twitch_table = str('CREATE TABLE twitch' +
                           '(twitchid PRIMARY KEY ASC,' +
                           'FOREIGN KEY(userid) REFERENCES user(userid)')

        cursor.execute(yt_table)
        cursor.execute(wpc_table)
        cursor.execute(livecode_table)
        cursor.execute(twitch_table)

        user_table = str('CREATE TABLE user (' +
                         'userid integer PRIMARY KEY ASC,' +
                         'FOREIGN KEY(livecodingid) REFERENCES ' +
                         'livecoding(livecodingid) DEFAULT NULL,' +
                         'FOREIGN KEY(twitchid) REFERENCES ' +
                         'twitch(twitchid) DEFAULT NULL,' +
                         'FOREIGN KEY(watchpeoplecodeid) REFERENCES ' +
                         'watchpeoplecode(watchpeoplecodeid) DEFAULT NULL,' +
                         'FOREIGN KEY(youtubeid) REFERENCES ' +
                         'youtube(youtubeid) DEFAULT NULL,' +
                         'roleid integer FOREIGN KEY DEFAULT 0)')

        # create user table
        cursor.execute(usr_table)
        # create activity table
        cursor.execute('CREATE TABLE activities (activityid integer PRIMARY KEY ASC, name text)')
        # create roles table
        cursor.execute('CREATE TABLE roles (roleid integer PRIMARY KEY ASC, name text)')
        roles = [('anonymous'), ('user'), ('trusted_user'), ('admin')]
        cursor.executemany('INSERT INTO roles VALUES(?)', roles)
        cursor.execute("PRAGMA user_version = 1")
        cursor.commit()

class ListenerHandler(QtCore.QObject):
    listeners_signal = QtCore.pyqtSignal(str, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.listeners = []
        self.queue = asyncio.Queue()
        self.data_base = Database()

    def _init_database(self):
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()
        self.data_base.update_schema(cursor)
        cursor.close()

    def activities(self):
        # do some fancy parsing to get all the activities out of the listeners, with the class/module name as key
        pass

    def roles(self):
        return ('admin', 'trusted_user', 'user', 'anonymous')

    def assign_roles(self, user, role, platform=None):
        pass

    @asyncio.coroutine
    def handle_messages(self):
        while True:
            sender, message, platform = yield from self.queue.get()
            # user = AUTH(sender, platform)
            result = None
            if self.listeners:
                for listener in self.listeners:
                    try:
                        result = listener(message, user, self.authentication_function)
                    except:
                        pass

            if result:
                pass

    @QtCore.pyqtSlot(str, str)
    def listener_slot(self, sender, message, platform=None):
        self.queue.put((sender, message, platform))
