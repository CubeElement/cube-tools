import pandas as pd
import openpyxl
import sys
import os
from PyQt5.QtWidgets import QApplication, QFileDialog

import config as cfg

class Model():
    def __init__(self):
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
    # print(header_parser(mach_table_path["HERMLE 09"]))
    # headers_data = header_parser(cfg.machine_files["HERMLE 09"])
    # print(headers_data.values())


    def read_tooltable(self, toolt_file):
        '''Align imported tables with headers'''
        headers = self.header_parser(toolt_file)
        tools = pd.read_fwf(toolt_file, 
                            skiprows=2, skipfooter=1, names=headers.keys(), 
                            colspecs=list(headers.values()), index_col=None)# infer_nrows=1
        tools = tools.dropna(subset=["T"])
        tools = tools.astype({"T":int})
        return tools

    def magazin_tools(self):
        '''Find tools in the tool-table those are in magazine available'''
        
        # magazin_tools = pd_tools.loc[[i[4]=="1" for i in pd_tools["PLC"]]]
        # magazin_tools.set_index("T")
        # magazin_tools = magazin_tools.loc[:,['T', 'NAME', 'L', 'DOC']]
        # return magazin_tools

    def export_tooltable(self, path_field: str, selected_machines):
        '''Exports pandas-tables in various formats '''
        self.path_field = path_field
        self.selected_machines = selected_machines
        print(self.selected_machines, '-- a list of machines')
        for (sel_name, sel_path) in {(name, path) for name, path in cfg.tool_files.items() if name in selected_machines}:
            tools_table = self.read_tooltable(sel_path+'tool.t')
            tools_table.to_excel(self.path_field + "/" + sel_name + '.xlsx', index=False)
            # tools_table.to_csv(self.path_field + name + '.csv', index=False)
            # tools_table.to_json(self.path_field + name + '.json')
            # print(self.path_field + "/" + sel_name + '.json', " file to export")
        # for (name, path) in cfg.tool_files.items():
            # tools_table = self.read_tooltable(path+'tool_p.tch')
            # tools_table.to_excel(self.path_field + name + '_magazine.xlsx', index=False)
            # tools_table.to_csv(self.path_field + name + '_magazine.csv', index=False)
            # tools_table.to_json(self.path_field + name + '_magazine.json')
        print(self.path_field + ' folder to export has taken')
        message = "Export is complete"
        return message

# def run():
#     app = QApplication(sys.argv)
#     model = Model()
#     window = mainframe.CubeToolsGUI(model=model)
#     window.show()
#     sys.exit(app.exec_())
    
# if __name__ == '__main__':

#     run()
