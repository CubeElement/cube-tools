import pytest
from cubetools import config as cfg


def test_check_filelist_correct(main_model, test_tool_dir, test_toolt,
                               test_toolptch):
    cfg.path_to_cnc = {"MACHINE_01":str(test_tool_dir)}
    expected = {"MACHINE_01":str(test_tool_dir)}
    assert main_model.check_cnc_filepaths() == expected

@pytest.mark.parametrize("incorrect_path", [
    "random_string",
    12,
    "/hom/",
    "%",
    "A",
    "",
])

def test_check_filelist_incorrect(incorrect_path, main_model):
    mdl = main_model
    cfg.path_to_cnc = {"HERMLE_10":incorrect_path}
    assert mdl.check_cnc_filepaths() == {}

@pytest.mark.parametrize("possible_header", [
    {"FIRST":(0, 8),"SECOND":(8, 15),"THIRD":(15, 22)},
])
def test_header_parser(test_toolt, main_model, possible_header):
    assert main_model.parse_headers(test_toolt) == possible_header
