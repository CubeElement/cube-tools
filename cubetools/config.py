
# available machines tool.t-files with relative path to it
import pathlib

toolt_file = {"HERMLE 09":'./data-examples/tool_H09.t', 
              "HERMLE 10":'./data-examples/tool_H10.t'
              }

save_path = str(pathlib.Path().absolute()) + '/exported/'