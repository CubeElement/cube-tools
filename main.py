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
