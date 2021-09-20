import os
import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import (
                            QGridLayout, QPushButton, QLineEdit,
                            QListWidget, QFileDialog, QApplication,
                            QCheckBox, QGroupBox, QHBoxLayout,
                            QAbstractItemView, QDesktopWidget, QErrorMessage,
                            QTableView, QHeaderView
                            )
from PyQt5.QtGui import QFont, QIcon
from cubetools.model import Model, ToolSummaryTable
import cubetools.config as cfg


# export DISPLAY=:0 for Qt Display Connection
def display_start_fix():
    os.environ['DISPLAY'] = ':0'


class CubeToolsGUI(QWidget):
    def __init__(self, model=None):
        super().__init__()
        self.model = model
        self.setWindowTitle("CubeTools")
        self.setGeometry(200, 20, 300, 500)
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

        self.formats_chboxes = QGroupBox("Select formats")
        self.chbox_xlsx = QCheckBox("xlsx")
        self.chbox_csv = QCheckBox("csv")
        self.chbox_json = QCheckBox("json")
        hbox = QHBoxLayout()
        hbox.addWidget(self.chbox_xlsx)
        hbox.addWidget(self.chbox_csv)
        hbox.addWidget(self.chbox_json)
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
        self.path_field.setText(cfg.export_path)
        self.fileformats_selected = set()
        self.isMachlist = self.isExtlist = self.isPath = True

    def create_machinelist(self):
        return self.model.valid_cncfilelist.keys()

    def message_popup(self, message):
        popup = QErrorMessage()
        popup.showMessage(message)
        popup.exec_()

    def connect_signals(self):
        self.path_button.clicked.connect(self.set_savepath_slot)
        self.go_button.clicked.connect(self.export_slot)
        self.chbox_xlsx.stateChanged.connect(self.set_fileformats)
        self.chbox_csv.stateChanged.connect(self.set_fileformats)
        self.chbox_json.stateChanged.connect(self.set_fileformats)
        self.machine_list.doubleClicked.connect(self.show_summarytable)

    def set_fileformats(self):
        if (self.sender().isChecked() and self.sender().text()
           not in self.fileformats_selected):
            self.fileformats_selected.add(self.sender().text())
        elif self.sender().text() in self.fileformats_selected:
            self.fileformats_selected.remove(self.sender().text())

    def set_savepath_slot(self):
        default_savepath = cfg.export_path
        title_text = 'Select directory to export'
        self.savepath = str(QFileDialog.getExistingDirectory(self,
                            title_text,
                            default_savepath))
        self.path_field.setText(self.savepath)

    def get_machines_slot(self) -> list:
        machines_selected = list(item.text()
                                for item
                                in self.machine_list.selectedItems())
        if machines_selected != list():
            self.isMachlist = True
            return machines_selected
        else:
            self.isMachlist = False
            self.message_popup("No machines selected to export")
            return machines_selected

    def get_fileformats(self) -> set:
        if self.fileformats_selected != set():
            self.isExtlist = True
            return self.fileformats_selected
        else:
            self.isExtlist = False
            self.message_popup("No extensions selected to export")
            return self.fileformats_selected

    def get_savepath_slot(self) -> str:
        path_to_export = self.path_field.text()
        if path_to_export != "":
            self.isPath = True
            return path_to_export
        else:
            self.isPath = False
            self.message_popup("Path to save can not be empty")

    def export_slot(self):
        machlist = self.get_machines_slot()
        extlist = self.get_fileformats()
        path = self.get_savepath_slot()
        if self.isMachlist == self.isExtlist == self.isPath == True:
            self.model.export_tooltable(machlist, extlist, path)
            self.message_popup("Export complete!")
        else:
            self.message_popup("Export failed")

    def show_summarytable(self):
        dclickeditem = self.machine_list.currentItem().text()
        self.toolsummary_data = ToolSummaryTable(dclickeditem)
        self.maintable_view = QTableView()
        header = self.maintable_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.maintable_view.resize(800, 600)
        self.maintable_view.setWindowTitle(dclickeditem)
        self.maintable_view.setModel(self.toolsummary_data)
        self.maintable_view.show()


def run():
    app = QApplication(sys.argv)
    model = Model()
    window = CubeToolsGUI(model=model)
    window.show()
    sys.exit(app.exec_())
