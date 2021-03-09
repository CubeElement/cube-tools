import pytest
from cubetools import model

@pytest.fixture
def main_model():
    mdl = model.Model()
    return mdl

@pytest.fixture
def test_toolt():
    test_open = '/home/erebor/git-workflow/cube-tools/cubetools/tests/test_tool.t'
    return test_open
