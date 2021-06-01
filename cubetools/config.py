
# available machines tool.t-files with relative path to it
import pathlib
import pandas as pd


pd.set_option('max_columns', None)
pd.set_option('max_rows', None)

path_to_cnc = {"MACHINE_01":'./data-examples/HERMLE_10/', 
              "MACHINE_02":'./data-examples/HERMLE_09/'
              }

export_path = str(pathlib.Path().absolute()) + '/exported'

refdb_sample = pd.DataFrame(
    {
        "T": pd.Series([2, 100, 110, 201, 202], dtype="int64"),
        "L_NOM": pd.Series([120, 5, 140, 100, 90], dtype="float64")
    }
)
