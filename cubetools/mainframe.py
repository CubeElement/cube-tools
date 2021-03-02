# export DISPLAY=:0 - command for Qt Display Connection errors

import os
import sys
from PyQt5.QtCore import Qt, QAbstractTableModel, QTimer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import (
                            QGridLayout, QPushButton, QLineEdit, 
                            QListWidget, QFileDialog, QApplication, 
                            QCheckBox, QGroupBox, QHBoxLayout,
                            QAbstractItemView, QDesktopWidget, QErrorMessage,
                            QTableView, QVBoxLayout
                            )
from PyQt5.QtGui import QFont, QIcon

from functools import partial
from cubetools.model import Model, MainTable_model
import cubetools.config as cfg

def display_start_fix():
    os.environ['DISPLAY'] = ':0'

class CubeToolsGUI(QWidget):
    def __init__(self, model=None):
        super().__init__()
        self.model = model
        self.setWindowTitle("CubeTools")
        self.setGeometry(2000, 20, 300, 500)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.ui_items()
        self.center_ui()
        self.reset_ui()
        self.connect_signals()
        self.new_window = None

    def ui_items(self):
        font = QFont()
        font.setFamily("Font Awesome 5 Free")
        font.setPointSize(20)

        self.path_button = QPushButton()
        self.path_button.setIcon(QIcon("./resources/folder-icon.png"))
        self.layout.addWidget(self.path_button, 1, 1, 1, 2)

        self.path_field = QLineEdit()
        self.layout.addWidget(self.path_field, 1, 0, 1, 1)


        self.machine_list = QListWidget(self)
        self.machine_list.setFont(font)
        self.machine_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.machine_list.insertItems(0, self.create_machinelist())
        self.layout.addWidget(self.machine_list, 0, 0, 1, -1)

        # self.go_button = QPushButton("GO!", self)
        # self.go_button.setGeometry(0, 0, 5, 5)
        # self.layout.addWidget(self.go_button, 2, 2)

        self.formats_chboxes = QGroupBox("Select formats")
        self.chbox1 = QCheckBox("xlsx")
        self.chbox2 = QCheckBox("csv")
        self.chbox3 = QCheckBox("json")
        hbox = QHBoxLayout()
        hbox.addWidget(self.chbox1)
        hbox.addWidget(self.chbox2)
        hbox.addWidget(self.chbox3)
        self.formats_chboxes.setLayout(hbox)
        self.layout.addWidget(self.formats_chboxes, 2, 0, 3, -1)

        self.go_button = QPushButton("EXPORT")
        self.layout.addWidget(self.go_button, 5, 0, 5, -1)

    def center_ui(self):
        pos = self.frameGeometry()
        cpoint = QDesktopWidget().availableGeometry().center()
        pos.moveCenter(cpoint)
        self.move(pos.topLeft())

    def reset_ui(self):
        self.path_field.setText(cfg.save_path)
        self.fileformat_selected = set()

    def create_machinelist(self):
        return self.model.checked_files.keys()

    def error_message_popup(self, message):
        error_dialog = QErrorMessage()
        error_dialog.showMessage(message)
        error_dialog.exec_()

    def connect_signals(self):
        self.path_button.clicked.connect(self.set_savepathSlot)
        self.go_button.clicked.connect(self.exportSlot)
        self.machine_list.itemSelectionChanged.connect(self.retrieve_machinesSlot)
        self.chbox1.stateChanged.connect(self.set_fileformats)
        self.chbox2.stateChanged.connect(self.set_fileformats)
        self.chbox3.stateChanged.connect(self.set_fileformats)
        self.machine_list.doubleClicked.connect(self.show_maintable)

    def set_fileformats(self):
        if self.sender().isChecked() and self.sender().text() not in self.fileformat_selected:
            self.fileformat_selected.add(self.sender().text())
            # print(self.ext_set, " item added")
        elif self.sender().text() in self.fileformat_selected:
            self.fileformat_selected.remove(self.sender().text())
            # print(self.ext_set, " item removed")
        return self.fileformat_selected

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

    def exportSlot(self):
        self.machines_selected = list(item.text() for item in self.machine_list.selectedItems())
                                      
        export_result = self.model.export_tooltable(self.get_savepathSlot(), 
                                    self.machines_selected,
                                    self.fileformat_selected
                                    )
        
        self.error_message_popup(export_result)
    def show_maintable(self):
        dclickeditem = self.machine_list.currentItem().text()
        self.new_model = MainTable_model(dclickeditem)
        self.maintable_view = QTableView()
        self.maintable_view.resize(800, 600)
        self.maintable_view.setWindowTitle(dclickeditem)
        self.maintable_view.setModel(self.new_model)
        self.maintable_view.show()


def run():
    app = QApplication(sys.argv)
    model = Model()
    window = CubeToolsGUI(model=model)
    window.show()
    sys.exit(app.exec_())
