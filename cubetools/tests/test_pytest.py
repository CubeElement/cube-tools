import pytest
# from cubetools import model
from cubetools import config as cfg
import os

@pytest.mark.parametrize("correct_path", [
    "./data-examples/HERMLE_10/",
])

def test_check_filelist_correct(correct_path, main_model):
    mdl = main_model
    cfg.tool_files = {"HERMLE_10":correct_path}
    expected = {"HERMLE_10":correct_path}
    assert mdl.check_filelist() == expected

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
    cfg.tool_files = {"HERMLE_10":incorrect_path}
    assert mdl.check_filelist() == {}

@pytest.mark.parametrize("possible_header", [
    {"FIRST":(0, 8),"SECOND":(8, 15),"THIRD":(15, 22)},
])
def test_header_parser(test_toolt, main_model, possible_header):
    mdl = main_model
    assert mdl.header_parser(test_toolt) == possible_header