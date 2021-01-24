# %%
import pandas as pd
import openpyxl
import os

pd.set_option('max_columns', None)
pd.set_option('max_rows', None)

# %%
with open('./data-examples/tool_H10.t') as data_table:
    table = data_table.readlines()
    names = table[1].split()
    colspecs_array = []
    prev_i = int()
    for i, k in enumerate(table[1]):
        if k!=" ":
            if (i!=prev_i+1):
                colspecs_array.append(i)
            prev_i = i
    colspecs_tuples = [(colspecs_array[i], colspecs_array[i+1]) for i in range(len(colspecs_array)-1)]

# %%
print(colspecs_tuples)
len(colspecs_array)

# %%
# widths = [9,    32,     12,  12,  12,   10,   10,   10,    11,     6,       6,       9,          9,     32,    10,    12,      8,       4,     7,      7,      7,       7,        12,       12,       7,        7,        10,     8,         7,       8,         21,         5,      8,         10,   7,    7,    7,    7,    7,    7,    7,    10,    4,     8,       9,          10,          10,          20,          10,         8]
# widths = ['T', 'NAME', 'L', 'R', 'R2', 'DL', 'DR', 'DR2', 'TLRT', 'TIME1', 'TIME2', 'CUR_TIME', 'TYP', 'DOC', 'PLC', 'LCUTS', 'ANGLE', 'CUT', 'LTOL', 'RTOL', 'R2TOL', 'DIRECT', 'R-OFFS', 'L-OFFS', 'LBREAK', 'RBREAK', 'NMAX', 'LIFTOFF', 'TP_NO', 'T-ANGLE', 'LAST_USE', 'PTYP', 'PLC-VAL', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'AFC', 'ACC', 'PITCH', 'AFC-LOAD', 'AFC-OVLD1', 'AFC-OVLD2', 'KINEMATIC', 'DR2TABLE', 'OVRTIME']
# names = ['T', 'NAME', 'L', 'R', 'R2', 'DL', 'DR', 'DR2', 'TLRT', 'TIME1', 'TIME2', 'CUR_TIME', 'TYP', 'DOC', 'PLC', 'LCUTS', 'ANGLE', 'CUT', 'LTOL', 'RTOL', 'R2TOL', 'DIRECT', 'R-OFFS', 'L-OFFS', 'LBREAK', 'RBREAK', 'NMAX', 'LIFTOFF', 'TP_NO', 'T-ANGLE', 'LAST_USE', 'PTYP', 'PLC-VAL', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'AFC', 'ACC', 'PITCH', 'AFC-LOAD', 'AFC-OVLD1', 'AFC-OVLD2', 'KINEMATIC', 'DR2TABLE', 'OVRTIME']
tools = pd.read_fwf(r'./data-examples/tool_H09.t',
                    skiprows=2, skipfooter=1, names=names, colspecs=colspecs_tuples, index_col=None)# infer_nrows=1
tools = tools.astype({"T":int})
# %%
tools.info()

# %%
tools.loc[1, 'NAME']
# %%
magazin_tools = tools.loc[[i[4]=="1" for i in tools["PLC"]]]

# %%
magazin_tools.set_index("T")
magazin_tools = magazin_tools.loc[:,['T', 'NAME', 'L', 'DOC']]
# %%
magazin_tools.to_excel(r'./exported/MagazinXX.xls', index=False)
magazin_tools.to_csv(r'./exported/MagazinXX.csv', index=False)
magazin_tools.to_json(r'./exported/MagazinXX.json')

# %%
import os
machine_filelist = os.listdir('input')
print(machine_filelist)
# %%
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

machine_filelist = os.listdir('input')

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

        path_button = QPushButton()
        self.layout.addWidget(path_button, 0, 0, 1, 1)


        label = QLabel()
        label.setText("Path_to")
        self.layout.addWidget(label, 0, 1, 1, 2)

        machine_list = QListWidget(self)
        machine_list.setGeometry(5, 30, 240, 300)
        machine_list.insertItems(0, self.machines)
        machine_list.setFont(font)
        # machine_list.setUniformItemSizes(True)
        # machine_list.setWordWrap(True)
        self.layout.addWidget(machine_list, 1, 0, 1, -1)

        go_button = QPushButton("GO!")
        go_button.setGeometry(0, 0, 30, 20)
        self.layout.addWidget(go_button, 2, 1)

app = QApplication(sys.argv)
window = CubeTools(machine_filelist)
sys.exit(app.exec_())

# %%
