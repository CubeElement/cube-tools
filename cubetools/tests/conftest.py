import pytest
from cubetools import model


TOOLT_CONTENT = "first line\nT       NAME   THIRD "
TOOLPTCH_CONTENT = " "

@pytest.fixture
def main_model():
    mdl = model.Model()
    return mdl

@pytest.fixture(scope="session")
def test_tool_dir(tmp_path_factory):
    tool_files_dir = tmp_path_factory.mktemp("tool_files")
    return tool_files_dir

@pytest.fixture(scope="session")
def test_toolt(tmp_path_factory, test_tool_dir):
    toolt = test_tool_dir / "tool.t"
    toolt.write_text(TOOLT_CONTENT)
    return toolt

@pytest.fixture(scope="session")
def test_toolptch(tmp_path_factory, test_tool_dir):
    toolptch = test_tool_dir / "tool_p.tch"
    toolptch.write_text(TOOLPTCH_CONTENT)
    return toolptch
