"""This script provides tools to handle an information from 
CNC controls by Heidenhain (TNC530 files have been tested)
By default tool.t (located on the CNC-Control) stores parameters for 
everything a machine knows about all created cutting tools profiles
(tool.t is fixed-width-field(fwf) text-file without any encryption)
Additionally, theres istool_p.tch provides a slot# in the machine for each available tool
The parameters of the tool.t-file are described in Manual to any TNC530-Control"""
import pandas as pd
import openpyxl
import sys
import os
import re
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant

import cubetools.config as cfg

class Model():
    '''Class contains the logic only without any UI elements handlers.
    Creates data for the main UI window and direct export'''
    def __init__(self):
        super().__init__()
        self.dir_regex = r"^[a-zA-Z0-9/_.-]+$"
        # import pdb; pdb.set_trace()
        self.checked_files = self.check_filelist()

    def check_filelist(self):
        '''Checks filepaths from config.py 
        
        Looked for tool-files in defined folders, and sorts off 
        inelegible values 

        Returns:
        dict: {NAME:PATH} format of the checked machine entries from cfg'''
        filelist = {}
        if cfg.tool_files:
            for name, dir_path in cfg.tool_files.items():
                str_dir = str(dir_path)
                dir_match = re.match(self.dir_regex, str_dir)
                is_matched = bool(dir_match)
                if is_matched is not False:
                    if (os.path.isfile(str_dir + 'tool.t') and 
                    os.path.isfile(str_dir + 'tool_p.tch')):
                        filelist[name] = str_dir
                else:
                    return {}
            if not filelist:
                return {}
            return filelist

    def header_parser(self, toolt_file):
        '''Gets headers indexes to define column widths

        Gets from headers line of a tool-file predefined 
        (by control manufacturer) widths of columns

        Parameters:
            toolt_file(file): full path fwf(fixed-width-field) file

        Returns:
            colspecs_dict(dict): columns {<COL_NAME>: (i_start, i_end)} formatted'''
        colspecs_dict = {}
        headers_line = []
        with open(toolt_file) as data_table:
            table = data_table.readlines()
            headers_line = table[1]
            names = headers_line.split()
            col_idx = []
            prev_i = 0
            for i, k in enumerate(headers_line): 
                if k!=" ":
                    if (i!=prev_i+1):
                        col_idx.append(i)
                    prev_i = i
            col_idx.append(len(headers_line)+1) # the last element index
            colspecs_dict = {name:(col_idx[i], col_idx[i+1]) 
                                    for (name, i) 
                                    in zip(names, range(len(col_idx)-1))
                }
        return colspecs_dict
        
    def read_tooltable(self, toolt_file):
        '''Reads tool-file into pandas-dataframe

        Parameters:
            toolt_file(file): full path fwf(fixed-width-field) file

        Returns:
            tools(dataframe): pandas dataframe with all cols/rows'''
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
        '''Exports pandas-tables in various formats

        Parameters:
        path_field(str): path for the exported files
        machines_selected(list): list of names to search for in the cfg
        fileformat_selected(list): list of extensions to export
        
        Returns:
        (str): message variable'''
        self.path_field = path_field
        self.machines_selected = machines_selected
        self.fileformat_selected = fileformat_selected
        self.fileformat_allowed = ['xlsx', 'csv', 'json']
        print(self.machines_selected, '-- a list of machines')
        print(self.fileformat_selected, '-- extensions')
        print(self.path_field + ' folder to export has taken')

        self.machines_checked = {(name, path) for name, path in self.checked_files.items() 
                                  if name in self.machines_selected}
        
        for sel_name, sel_path in self.machines_checked:
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
                    return "Export is complete"
            else:
                return "No extension(s) selected"
        else:
            return "No machine(s) selected"
            
class MainTable_model(QAbstractTableModel, Model):
    '''Provides a table data for a preview window before an actual export.'''
    def __init__(self, machine_selected):
        super().__init__()
        self.machine_selected = machine_selected
        if self.machine_selected in self.checked_files.keys():
            self.tool_file = self.checked_files[self.machine_selected]
            print(self.tool_file)
        mainmodel = Model()
        self.tooldf = mainmodel.read_tooltable(self.tool_file + "tool.t")
        self.magazindf = mainmodel.read_tooltable(self.tool_file + "tool_p.tch")
        self.dfmerged = self.tooldf.loc[self.tooldf['T'].isin(self.magazindf['T'])]
        self.dfmerged = self.dfmerged[['T', 'NAME', 'DOC']]

    # standart requiered methods to describe a QAbstractModel subclass
    def rowCount(self, index):
        return self.dfmerged.shape[0]

    def columnCount(self, index):
        return self.dfmerged.shape[1]

    def data(self, index, role):
        if role != Qt.DisplayRole:
            return QVariant()
        return str(self.dfmerged.iloc[index.row(), index.column()])
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        return self.dfmerged.columns[section]
