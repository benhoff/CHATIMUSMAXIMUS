import os
from enum import Enum
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from gui import MessageArea

class MainWindow(QtWidgets.QMainWindow):
    _time_signal = QtCore.pyqtSignal(str)

    class StatusBarSelector(Enum):
        Youtube = 0
        Twitch = 1
        Livecoding = 2
        WatchPeopleCode = 3

    def __init__(self, parent=None):
        """
        MainWindow uses a QTextEdit to display chat
        """
        # initialize parent class. Req'd for PyQt subclasses
        super(MainWindow, self).__init__(parent)

        # set title window to `CHATIMUSMAXIMUS`
        self.setWindowTitle("CHATIMUSMAXIMUS")
        
        # create the text edit used to display the text
        self.message_area = MessageArea(parent=self) 

        # duck type the slot onto the MainWindow for ease of access
        self.chat_string_slot = self.message_area.chat_string_slot
        
        # tried to set the background to be transparent
        # does not work without a compositor in Linux
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setStyleSheet('background: transparent;')
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # create vertical layout to stack the textedit on top
        # of the `clear` button 
        vertical_layout = QtWidgets.QVBoxLayout()
        
        # create `clear` button
        button = QtWidgets.QPushButton("CLEAR")
        button.setStyleSheet('color: white;')
        button.clicked.connect(self.message_area.clear)
        
        # add the text edit and button to vertical layout
        vertical_layout.addWidget(self.message_area)
        vertical_layout.addWidget(button)
        
        # create a widget to set the layout to be 
        # the vertical layout created above
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(vertical_layout)

        self.setCentralWidget(central_widget)

        # sets name and text formats
        self.name_format = None
        self.text_format = None
        self._set_up_text_formats()

        # set up the status widgets
        self._file_dir = os.path.realpath(os.path.dirname(__file__))
        self._status_widgets = []
        time_label = QtWidgets.QLabel()
        time_label.setStyleSheet('color: white;')

        self._time_signal.connect(time_label.setText)
        self.statusBar().addPermanentWidget(time_label)

    def set_settings(self, settings):
        for key, settings in settings.items():
            display_setting = setting['display_setting']
            if display_settings['display_missing']:
                self._set_up_status_bar_helper(key.title)
            if display_settings['text_color']:
                self.message_area.set_color(display_settings['text_color'])

    def _set_up_status_bar_helper(self, platform_name):
        status_bar = self.statusBar()
        red_button = os.path.join(self._file_dir, 'resources', 'red_button.png')
        button = QtWidgets.QPushButton(QtGui.QIcon(red_button), 
                                       ' ' + platform_name)

        button.setFlat(True)
        button.setAutoFillBackground(True)
        button.setStyleSheet('color: white;')
        status_bar.addPermanentWidget(button)
        self._status_widgets.append(button)

        #self.setStatusBar(status_bar)
    
    @QtCore.pyqtSlot(int, bool)
    def set_status_widget_status(self, service_index, bool):
        # get the appropriate status widget
        button = self._status_widgets[service_index]
        if bool:
            # if activate, set green
            green_button = os.path.join(self._file_dir, 
                                        'resources', 
                                        'green_button.png')

            button.setIcon(QtGui.QIcon(green_button))
        else:
            # else set it to be red
            red_button = os.path.join(self._file_dir, 
                                      'resources', 
                                      'red_button.png')

            button.setIcon(red_button)
