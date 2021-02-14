
# available machines tool.t-files with relative path to it
import pathlib
import pandas as pd


pd.set_option('max_columns', None)
pd.set_option('max_rows', None)

tool_files = {"HERMLE_10":'./data-examples/HERMLE_10/', 
              "HERMLE_09":'./data-examples/HERMLE_09/'
              }


save_path = str(pathlib.Path().absolute()) + '/exported'