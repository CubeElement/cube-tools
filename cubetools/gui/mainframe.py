# export DISPLAY=:0 - command for Qt Display Connection errors

import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout, QPushButton, QLineEdit, QListWidget
from PyQt5.QtGui import QFont


class CubeToolsGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CubeTools")
        self.setGeometry(2000, 20, 250, 250)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.ui_items()
        self.show()

    def ui_items(self):
        font = QFont()
        font.setFamily("Font Awesome 5 Free")
        font.setPointSize(20)

        self.path_button = QPushButton()
        self.layout.addWidget(self.path_button, 0, 0, 1, 1)

        self.path_field = QLineEdit()
        self.layout.addWidget(self.path_field, 0, 1, 1, 2)

        self.machine_list = QListWidget(self)
        # machine_list.insertItems(0, ['MACH2', 'MACH2'])
        self.machine_list.setFont(font)
        self.layout.addWidget(self.machine_list, 1, 0, 1, -1)

        self.go_button = QPushButton("GO!", self)
        self.go_button.setGeometry(0, 0, 30, 20)
        self.layout.addWidget(self.go_button, 2, 2)
    
    def export_all(self):
        print('Hello!')

        # settings_button = QPushButton("Settings")
        # settings_button.setGeometry(0, 0, 30, 20)
        # self.layout.addWidget(settings_button, 2, 0)

        # TODO separate functions from ui_items
        # self.connectSignals()

    # def connectSignals(self):
    #     self.export_all()
    #     self.go_button.clicked.connect(self.export_all)

    # def export_all(self):
    #     print('Hello')