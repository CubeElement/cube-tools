import pandas as pd
import openpyxl
import sys
import os
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant

import config as cfg

class Model():
    def __init__(self):
        super().__init__()
        self.check_filelist()

    def check_filelist(self):
        filelist = {name: dir_path for name, dir_path in cfg.tool_files.items() 
                        if os.path.isfile(dir_path + 'tool.t') and os.path.isfile(dir_path + 'tool_p.tch')}
        return filelist

    def header_parser(self, toolt_file):
        '''Parse headers indexes to define column widths.'''
        colspecs_dict = {}
        with open(toolt_file) as data_table:
            table = data_table.readlines()
            names = table[1].split()
            col_idx = []
            prev_i = int()
            for i, k in enumerate(table[1]): # headers line in the .t-files
                if k!=" ":
                    if (i!=prev_i+1):
                        col_idx.append(i)
                    prev_i = i
            colspecs_dict = {
                name:(col_idx[i], col_idx[i+1]) for (name, i) in zip(names, range(len(col_idx)-1))
                }
        return colspecs_dict
        
    def read_tooltable(self, toolt_file):
        '''Align imported tables with headers'''
        headers = self.header_parser(toolt_file)
        tools = pd.read_fwf(toolt_file, 
                            skiprows=2, skipfooter=1, names=headers.keys(), 
                            colspecs=list(headers.values()), index_col=None)# infer_nrows=1
        tools = tools.dropna(subset=["T"])
        tools = tools.astype({"T":int})
        return tools

    def export_tooltable(self,  
                         path_field: str, 
                         machines_selected: list, 
                         fileformat_selected: list):
        '''Exports pandas-tables in various formats '''
        self.path_field = path_field
        self.machines_selected = machines_selected
        self.fileformat_selected = fileformat_selected
        self.fileformat_allowed = ['xlsx', 'csv', 'json']
        print(self.machines_selected, '-- a list of machines')
        print(self.fileformat_selected, '-- extensions')
        print(self.path_field + ' folder to export has taken')

        self.machines_checked = {(name, path) for name, path in cfg.tool_files.items() 
                                  if name in self.machines_selected}

        for (sel_name, sel_path) in self.machines_checked:
            tools_table = self.read_tooltable(sel_path+'tool.t')
            magazin_table = self.read_tooltable(sel_path+'tool_p.tch')
            
            for ext in self.fileformat_selected:
                if ext in self.fileformat_allowed:
                    if ext=="xlsx": 
                        tools_table.to_excel(self.path_field + "/" + sel_name + '.xlsx', index=False)
                        magazin_table.to_excel(self.path_field + "/" + sel_name + '_magazine.xlsx', index=False)
                    if ext=="csv":
                        tools_table.to_csv(self.path_field + "/" + sel_name + '.csv', index=False)
                        magazin_table.to_csv(self.path_field + "/" + sel_name + '_magazine.csv', index=False)
                    if ext=="json":
                        tools_table.to_json(self.path_field + "/" + sel_name + '.json')
                        magazin_table.to_json(self.path_field + "/" + sel_name + '_magazine.json')

        # message = "Export is complete"
        # return message

class MainTable_model(QAbstractTableModel, Model):
    def __init__(self, machine_selected):
        super().__init__()
        self.machine_selected = machine_selected
        # self.headers = ["Scientist name", "Birthdate", "Contribution"]
        # self.rows =    [("Newton", "1643-01-04", "Classical mechanics"),
        #    ("Einstein", "1879-03-14", "Relativity"),
        #    ("Darwin", "1809-02-12", "Evolution")]
        if self.machine_selected in cfg.tool_files.keys():
            self.tool_file = cfg.tool_files[self.machine_selected]
            print(self.tool_file)
        mainmodel = Model()
        self.data_ex = mainmodel.read_tooltable(self.tool_file + "tool.t")
        self.rows = self.data_ex["NAME"]

    def rowCount(self, index):
        return self.data_ex.shape[0]

    def columnCount(self, index):
        return self.data_ex.shape[1]

    def data(self, index, role):
        if role != Qt.DisplayRole:
            return QVariant()
        return str(self.data_ex.iloc[index.row(), index.column()])
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        return self.data_ex.columns[section]