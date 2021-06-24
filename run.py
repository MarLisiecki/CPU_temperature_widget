# -*- coding: utf-8 -*-
# @Time    : 24.06.2021
# @Author  : Marcin Lisiecki
# @Software: PyCharm

import sys

from PySide2 import QtCore
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from cpu_temp.cpu_temp import CPU_temp
from screens.ui_loading_screen import Ui_LoadingScreen
from widgets import CircularProgress


class CPU_widget(QMainWindow):
    def __init__(self):
        # Setup main loading screen
        QMainWindow.__init__(self)
        self.ui = Ui_LoadingScreen()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.draggable = True
        self.dragging_threshould = 5
        self.__mouse_pressed_position = None
        self._mouse_move_positions = None
        # Create progress bar
        self.progress = CircularProgress()
        self.progress.width = 300
        self.progress.height = 300
        self.progress.value = 0
        self.progress.move(25, 25)
        self.progress.setFixedSize(self.progress.width, self.progress.height)
        self.progress.add_shadow(True)
        self.progress.font_size = 16
        self.progress.setParent(self.ui.centralwidget)
        self.progress.show()
        # Crete timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(25)

        self.show()

    def update_status(self) -> None:
        """
        Function which updates temperature level and set value of actual temperature

        :return: None
        """
        cpu_temp = CPU_temp()
        temp = cpu_temp.read_cpu_package_temp()
        self.progress.set_value(int(temp))

    def mousePressEvent(self, event) -> None:
        """
        Function which detects mouse event and set positioning variables

        :param event: QMouseEvent
        :return: None
        """
        if self.draggable and event.button() == QtCore.Qt.LeftButton:
            self.__mouse_pressed_position = event.globalPos()  # global
            self._mouse_move_positions = event.globalPos() - self.pos()  # local
        super(CPU_widget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        """
        Function which set new positioning variables and allows you to change position of the widget

        :param event: QMouseEvent
        :return:
        """
        if self.draggable and event.buttons() & QtCore.Qt.LeftButton:
            global_position = event.globalPos()
            moved = global_position - self.__mouse_pressed_position

            if moved.manhattanLength() > self.dragging_threshould:
                difference = global_position - self._mouse_move_positions
                self.move(difference)
                self._mouse_move_positions = global_position - self.pos()
        super(CPU_widget, self).mouseMoveEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CPU_widget()
    sys.exit(app.exec_())
