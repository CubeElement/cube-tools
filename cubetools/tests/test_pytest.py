import pytest
from cubetools import model
from cubetools import config as cfg

@pytest.mark.parametrize("incorrect_path", [
    "random_string", 
    12, 
    "/hom/", 
    "%",
    "A",
    "./data-examples/HERMLE_10/",
    "",
])

def test_check_filelist(incorrect_path):
    mdl = model.Model()
    cfg.tool_files = {"HERMLE_10":incorrect_path}
    expected = {"HERMLE_10": './data-examples/HERMLE_10/'}
    assert mdl.check_filelist() == False