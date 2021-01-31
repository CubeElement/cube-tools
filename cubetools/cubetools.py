import pandas as pd
import openpyxl
import os

class CTController():
    def __init__(self, view):
        self.view = view
        self.view.path_field.setText(cfg.save_path)
        self.view.machine_list.insertItems(0, list(cfg.toolt_file.keys()))
        self.connectSignals()

    def connectSignals(self):
        self.view.go_button.clicked.connect(export_tooltable)




def header_parser(toolt_file):
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


def read_tooltable(toolt_file_path):
    
    headers = header_parser(toolt_file_path)
    pd.set_option('max_columns', None)
    pd.set_option('max_rows', None)
    tools = pd.read_fwf(toolt_file_path, 
                        skiprows=2, skipfooter=1, names=headers.keys(), 
                        colspecs=list(headers.values()), index_col=None)# infer_nrows=1
    tools = tools.astype({"T":int})
    return tools

# def magazin_tools(pd_tools):
#     '''Find tools in the tool-table those are in magazin available by 4th bit of 8-digit binary PLC-value'''   
#     magazin_tools = pd_tools.loc[[i[4]=="1" for i in pd_tools["PLC"]]]
#     magazin_tools.set_index("T")
#     magazin_tools = magazin_tools.loc[:,['T', 'NAME', 'L', 'DOC']]

def export_tooltable():
    toolt_filelist = cfg.toolt_file
    for (name, path) in toolt_filelist.items():
        tools_table = read_tooltable(path)
        tools_table.to_excel(r'./exported/' + name + '.xlsx', index=False)
        tools_table.to_csv(r'./exported/' + name + '.csv', index=False)
        tools_table.to_json(r'./exported/' + name + '.json')
        message = "Export complete"
    return message
    # print('EXPORTED!')

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    from gui import mainframe
    import config as cfg
    import sys

    def run():
        app = QApplication(sys.argv)
        window = mainframe.CubeToolsGUI()
        window.show()
        CTController(view=window)
        sys.exit(app.exec_())
    run()