"""
By default tool.t (located on the CNC-Control) stores parameters for
everything a machine knows about all created tools profiles
(tool.t is fixed-width-field(fwf) text-file without any encryption)
Additionally, tool_p.tch provides a slot# in a given machine for each of
available tools. The parameters of the tool.t-file are described in Manual to
any TNC530-Control"""
import pandas as pd
import numpy as np
import os
import re
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant

import cubetools.config as cfg


class Model():
    '''Creates data for the UI and export'''
    def __init__(self):
        super().__init__()
        self.valid_cncfilelist = self.check_cnc_filepaths()

    def check_cnc_filepaths(self):
        '''Checks filepaths from config.py

        Look for tool-files in defined folders, and sorts off
        inelegible values

        Returns:
        dict: {NAME:PATH} format of the checked machine entries from cfg'''
        filelist = {}
        if cfg.path_to_cnc:
            for name, dir_path in cfg.path_to_cnc.items():
                dir_path_string = str(dir_path)
                if (os.path.isfile(dir_path_string + '/tool.t') and
                   os.path.isfile(dir_path_string + '/tool_p.tch')):
                    filelist[name] = dir_path_string
            if not filelist:
                return {}
            return filelist

    def parse_headers(self, toolt_cncfile):
        '''Gets headers indexes to define column widths

        Parameters:
            toolt_cncfile(file): full path fwf(fixed-width-field) file

        Returns:
            colspecs_dict(dict): columns {<COL_NAME>: (i_start, i_end)} '''
        colspecs_dict = {}
        headers_line = []
        with open(toolt_cncfile) as data_toolt:
            table_toolt = data_toolt.readlines()
            headers_line = table_toolt[1]
            column_names = headers_line.split()
            col_idx = []
            prev_i = 0
            for i, k in enumerate(headers_line):
                if k != " ":
                    if (i != prev_i+1):
                        col_idx.append(i)
                    prev_i = i
            col_idx.append(len(headers_line)+1)  # index of the last element
            colspecs_dict = {name: (col_idx[i], col_idx[i+1])
                             for (name, i)
                             in zip(column_names, range(len(col_idx)-1))}
        return colspecs_dict

    def read_tooltable(self, toolt_cncfile):
        '''Reads tool-file into pandas-dataframe

        Parameters:
            toolt_cncfile(file): full path fwf(fixed-width-field) file

        Returns:
            dftools(dataframe): pandas dataframe with all cols/rows'''
        headers = self.parse_headers(toolt_cncfile)
        dftools = pd.read_fwf(toolt_cncfile,
                              skiprows=2, skipfooter=1, names=headers.keys(),
                              colspecs=list(headers.values()), index_col=None)
        dftools = dftools.dropna(subset=["T"])
        dftools = dftools.astype({"T": int})
        return dftools

    def export_tooltable(self,
                         path_field: str,
                         machines_selected: list,
                         fileformats_selected: set):
        '''Exports pandas-tables in various formats

        Parameters:
        path_field(str): path for the exported files
        machines_selected(list): list of names to search for in the cfg
        fileformats_selected(set): set of extensions to export

        Returns:
        (str): message text'''
        message = ''
        self.ui_path_field = path_field
        self.machines_selected = machines_selected
        self.fileformats_selected = fileformats_selected
        self.fileformats_allowed = {'xlsx', 'csv', 'json'}
        self.actual_machinelist = dict([(name, path) for name, path
                                        in self.valid_cncfilelist.items()
                                        if name in self.machines_selected])
        if self.actual_machinelist == dict():
            message = 'No machine (s) selected'
        for mach_name, dir_path in self.actual_machinelist.items():
            toolt = self.read_tooltable(dir_path+'tool.t')
            toolpt = self.read_tooltable(dir_path+'tool_p.tch')
            file_to_save = self.ui_path_field + "/" + mach_name
            if self.fileformats_selected:
                for ext in self.fileformats_selected:
                    if ext in self.fileformats_allowed:
                        if ext == "xlsx":
                            toolt.to_excel(file_to_save + '.xlsx',
                                           index=False)
                            toolpt.to_excel(file_to_save + '_magazine.xlsx',
                                            index=False)
                        if ext == "csv":
                            toolt.to_csv(file_to_save + '.csv',
                                         index=False)
                            toolpt.to_csv(file_to_save + '_magazine.csv',
                                          index=False)
                        if ext == "json":
                            toolt.to_json(file_to_save + '.json')
                            toolpt.to_json(file_to_save + '_magazine.json')
                message = 'Export is complete'
            else:
                message = 'No extension (s) selected'
        else:
            return message


class ToolSummaryTable(QAbstractTableModel, Model):
    '''Provides datatable for the preview'''
    def __init__(self, machine_selected):
        super().__init__()
        mainmodel = Model()
        self.machine_name = machine_selected
        if self.machine_name in self.valid_cncfilelist.keys():
            self.tool_file = self.valid_cncfilelist[self.machine_name]
        self.tooldf = mainmodel.read_tooltable(self.tool_file + "tool.t")
        self.magazindf = mainmodel.read_tooltable(self.tool_file + "tool_p.tch")
        self.summarydf = self.tooldf.loc[self.tooldf['T'].isin(self.magazindf['T'])]
        self.summarydf = self.summarydf[['T', 'NAME', 'DOC', "L"]]
        self.summarydf = self.assign_toolstatus(self.summarydf)

    def rowCount(self, index):
        return self.summarydf.shape[0]

    def columnCount(self, index):
        return self.summarydf.shape[1]

    def data(self, index, role):
        if role != Qt.DisplayRole:
            return QVariant()
        return str(self.summarydf.iloc[index.row(), index.column()])

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        return self.summarydf.columns[section]

    def assign_toolstatus(self, summarydf):
        refdb_df = cfg.refdb_sample
        summarydf['L_NOM'] = summarydf['T'].map(refdb_df.set_index('T')['L_NOM'])
        summarydf['Status'] = np.where(summarydf['L'] > summarydf['L_NOM'],
                                       'Check is failed',
                                       'Tool is OK')
        summarydf.loc[pd.isna(summarydf['L_NOM']) == True, 'Status'] = 'Not checked'

        return summarydf
