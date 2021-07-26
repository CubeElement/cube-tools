import pytest
import os
import pandas as pd
from cubetools import config as cfg


def test_check_filelist_correct(main_model, test_tool_dir, test_toolt,
                                test_toolptch):
    cfg.path_to_cnc = {"MACHINE_01": str(test_tool_dir)}
    expected = {"MACHINE_01": str(test_tool_dir)}
    assert main_model.check_cnc_filepaths() == expected


@pytest.mark.parametrize("possible_header",
    [{"T":(0, 8), "NAME":(8, 15), "THIRD":(15, 22)}]
)
def test_header_parser(test_toolt, main_model, possible_header):
    header_line = "T       NAME   THIRD "
    assert main_model.parse_headers(header_line) == possible_header


def test_read_tooltable(main_model, test_toolt):
    test_df = main_model.read_tooltable(test_toolt)
    excepted_df = pd.DataFrame(columns=["T", "NAME", "THIRD"])
    assert isinstance(test_df, pd.DataFrame)
    assert list(test_df.columns) == list(excepted_df.columns)


def test_export_tooltable(main_model, test_tool_dir, test_toolt, test_toolptch):
    machines = "MACHINE_01"
    exts = {"csv"}
    main_model.export_tooltable(machines, exts, test_tool_dir)
    assert (os.path.isfile(test_tool_dir / 'MACHINE_01.csv'))
    assert (os.path.isfile(test_tool_dir / 'MACHINE_01_magazine.csv'))
