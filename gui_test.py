import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *


machine_filelist = os.listdir('input')
print(machine_filelist)


class CubeTools(QWidget):
    def __init__(self, machines):
        super().__init__()
        self.machines = machines
        self.setWindowTitle("CubeTools")
        self.setGeometry(2000, 20, 250, 400)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.ui_items()
        self.show()

    def ui_items(self):

        font = QFont()
        font.setFamily("Font Awesome 5 Free")
        font.setPointSize(20)
        label = QLabel()
        label.setText("Path_to")
        self.layout.addWidget(label, 0, 0, 1, -1)
        machine_list = QListWidget(self)
        machine_list.setGeometry(5, 30, 240, 300)
        machine_list.insertItems(0, self.machines)
        machine_list.setFont(font)
        # machine_list.setUniformItemSizes(True)
        # machine_list.setWordWrap(True)
        self.layout.addWidget(machine_list, 1, 0, 1, -1)
        go_button = QPushButton("GO!")
        # go_button.setGeometry(0, 0, 30, 20)
        self.layout.addWidget(go_button, 2, 1)

app = QApplication(sys.argv)
window = CubeTools(machine_filelist)
sys.exit(app.exec_())