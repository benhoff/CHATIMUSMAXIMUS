import os
from PyQt5 import QtWidgets, QtGui, QtCore


class StatusBar(QtWidgets.QStatusBar):
    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent)
        file_dir = os.path.dirname(__file__)
        resource_dir = os.path.join(file_dir, 'resources', 'buttons')
        red_button = os.path.join(resource_dir, 'red_button.png')
        green_button = os.path.join(resource_dir, 'green_button.png')

        self._red_icon = QtGui.QIcon(red_button)
        self._green_icon = QtGui.QIcon(green_button)

        self.time_label = QtWidgets.QLabel()
        self.time_label.setStyleSheet('color: white;')

        self.addPermanentWidget(self.time_label)

        # set up the status widgets
        self._status_widgets = {}

    def set_up_helper(self, platform_name):
        button = QtWidgets.QPushButton(self._red_icon,
                                       ' ' + platform_name)

        button.setFlat(True)
        button.setAutoFillBackground(True)
        button.setStyleSheet('color: white;')
        self.addPermanentWidget(button)
        self._status_widgets[platform_name.lower()] = button

    @QtCore.pyqtSlot(bool, str)
    def set_widget_status(self, bool, platform_name):
        # get the appropriate status widget
        if platform_name:
            button = self._status_widgets[platform_name]
        else:
            return
        if bool:
            button.setIcon(self._green_icon)
        else:
            button.setIcon(self._red_icon)
