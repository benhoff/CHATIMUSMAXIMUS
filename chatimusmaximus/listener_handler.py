import asyncio
import sqlite3
from PyQt5 import QtCore
import sqlalchemy

engine = create_engine('sqlite:///:memory:', echo=True)



class Role(sqlalchemy.


class Database(object):
    VERSION = 1

    def update_schema(self, cursor):
        version = cursor.execute("PRAGMA user_version")
        if version.fetchone()[0] == 0:
            self.version_1(cursor)

    def version_1(self, cursor: sqlite3.Cursor):
        cursor.execute("PRAGMA foreign_keys = ON")

        role_table = 'CREATE TABLE role (name text, id INTEGER PRIMARY KEY AUTOINCREMENT)'

        youtube_table = '''CREATE TABLE youtube (name text UNIQUE, roleid integer, FOREIGN KEY(roleid) REFERENCES role(id))'''

        wpc_table = '''CREATE TABLE watchpeoplecode (name text UNIQUE, roleid integer, FOREIGN KEY(roleid) REFERENCES role(id))'''

        livecode_table = '''CREATE TABLE livecoding (name text UNIQUE, roleid integer, FOREIGN KEY(roleid) REFERENCES role(id))'''

        twitch_table = '''CREATE TABLE twitch (name text UNIQUE, roleid integer, FOREIGN KEY(roleid) REFERENCES role(id))'''

        # Create role table first!
        cursor.execute(role_table)
        # create the user table second!

        cursor.execute(youtube_table)
        cursor.execute(wpc_table)
        cursor.execute(livecode_table)
        cursor.execute(twitch_table)

        # create activity table
        cursor.execute('CREATE TABLE activity(id integer PRIMARY KEY AUTOINCREMENT, name text, roleid INTEGER, FOREIGN KEY(roleid) REFERENCES role(id))')
        # create roles table
        roles = (('anonymous',), ('user',), ('trusted_user',), ('admin',))
        cursor.executemany('INSERT INTO role(name) VALUES(?)', roles)
        cursor.execute("PRAGMA user_version = 1")
        # make sure our changes are committed
        connection.commit()

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
