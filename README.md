# cube-tools
### **cube-tools** is a small utility for faster and easier search and maintainability routines of a big tool-magazines/ToolDBs.

![comics_drawing](https://user-images.githubusercontent.com/70653782/111027069-3172e300-83ee-11eb-94f5-35be9ba1c12e.png)

Script offers simple UI with the machines list, formats and path to export.

![Screenshot from 2021-03-13 10-24-09](https://user-images.githubusercontent.com/70653782/111025715-4cd9f000-83e6-11eb-950d-f9404f2dd0f9.png)

Data analysis based on **pandas** library produces useful status overview for each tool in user's reference ToolDB (nominal and measured length compared).

![cubetools_preview_window_screenshot](https://user-images.githubusercontent.com/70653782/111025676-fa003880-83e5-11eb-992b-fd41370d9905.png)

It makes the information, that stored on machines in **tool.t** and **tool_p.tch**(fixed-width-field)\* files, available in popular fileformats such as csv, json or xlsx.

```
export listing
...
MACHINE_02.json
MACHINE_02_magazine.json
MACHINE_02.csv
MACHINE_02_magazine.csv
MACHINE_02.xlsx
MACHINE_02_magazine.xlsx
```

Furthermore these tables could be integrated in CAM-Based production processes, ot just provide to a CAM-Programmer current tool-magazine status in a table view-format on PC away from machines.



\* ***tool.t** and **tool_p.tch** are two "service" files located on the CNC-control HDD
First file saves all predefined parameters for every tool-entry such as type, diameter, length (see TNC-manual for more info)
Tool_p.tch on the other hand has only available in the machine-magazine list of tools (with actually measured length)*
