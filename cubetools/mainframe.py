# export DISPLAY=:0 - command for Qt Display Connection errors

import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout, QPushButton, QLineEdit, QListWidget, QFileDialog, QApplication, QAbstractItemView, QDesktopWidget, QErrorMessage
from PyQt5.QtGui import QFont, QIcon
from functools import partial
from model import Model
import config as cfg

def display_start_fix():
    os.environ['DISPLAY'] = ':0'

class CubeToolsGUI(QWidget):
    def __init__(self, model=None):
        super().__init__()
        self.model = model
        self.setWindowTitle("CubeTools")
        self.setGeometry(2000, 20, 300, 350)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.ui_items()
        self.center()
        self.reset_ui()
        self.connect_signals()
        self.show()

    def ui_items(self):
        font = QFont()
        font.setFamily("Font Awesome 5 Free")
        font.setPointSize(20)

        self.path_button = QPushButton()
        self.path_button.setIcon(QIcon("./resources/folder-icon.png"))
        self.layout.addWidget(self.path_button, 0, 0, 1, 1)

        self.path_field = QLineEdit()
        self.layout.addWidget(self.path_field, 0, 1, 1, 2)


        self.machine_list = QListWidget(self)
        self.machine_list.setFont(font)
        self.machine_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.machine_list.insertItems(0, self.create_machinelist())
        self.layout.addWidget(self.machine_list, 1, 0, 1, -1)

        self.go_button = QPushButton("GO!", self)
        self.go_button.setGeometry(0, 0, 30, 20)
        self.layout.addWidget(self.go_button, 2, 2)

        # settings_button = QPushButton("Settings")
        # settings_button.setGeometry(0, 0, 30, 20)
        # self.layout.addWidget(settings_button, 2, 0)

    def center(self):
        pos = self.frameGeometry()
        cpoint = QDesktopWidget().availableGeometry().center()
        pos.moveCenter(cpoint)
        self.move(pos.topLeft())

    def reset_ui(self):
        self.path_field.setText(cfg.save_path)
        pass

    def create_machinelist(self):
        checked_machinelist = self.model.check_filelist().keys() 
        if checked_machinelist:
            return self.model.check_filelist().keys()   
        else:
            self.error_message("No files tool.t and tool_p.tch found")
            return []
    def error_message(self, message):
        error_dialog = QErrorMessage()
        error_dialog.showMessage(message)
        error_dialog.exec_()

    def connect_signals(self):
        self.path_button.clicked.connect(self.set_savepathSlot)
        self.go_button.clicked.connect(self.exportSlot)
        self.machine_list.itemSelectionChanged.connect(self.retrieve_machinesSlot)  

    def retrieve_machinesSlot(self):
        for name in self.machine_list.selectedItems():
            print(name.text(), sep = "&", end = " ", flush=True)

    def set_savepathSlot(self):
        default_savepath = cfg.save_path
        title_text = 'Select directory to export'
        self.savepath = str(QFileDialog.getExistingDirectory(self, 
                            title_text, 
                            default_savepath))

        self.path_field.setText(self.savepath)
        print(self.path_field.text(), 'savepath is set')
        return self.path_field.text()

    def get_savepathSlot(self):
        return self.path_field.text()

    # def print_save_path(self):
    #     print(self.path_field.text())

    def exportSlot(self):
        self.selected_machines = list(item.text() for item in self.machine_list.selectedItems())
                                      
        self.model.export_tooltable(self.get_savepathSlot(), 
                                    self.selected_machines)

def run():
    app = QApplication(sys.argv)
    model = Model()
    window = CubeToolsGUI(model=model)
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    display_start_fix()
    run()