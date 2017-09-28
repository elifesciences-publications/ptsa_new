import pytest
from ptsa.helper import standardize_label

@pytest.mark.parametrize("input,expected_output",[
    ("LAD1", "LAD1"),
    ("LAD1-LAD2", "LAD1-LAD2"),
    ("RHD10-RHD11", "RHD10-RHD11"),
    ("LAD 1", "LAD1"),
    ("LAD \t 1", "LAD1"),
    ("LAD \n 1", "LAD1"),
    ("LAD01", "LAD1"),
    ("LAD09-LAD10", "LAD9-LAD10"),
    ("RAHDmicro1", "RAHDMICRO1"),
    ("RAHDmicro9-RAHDmicro10", "RAHDMICRO9-RAHDMICRO10"),
    ("LAd1", "LAD1"),
    ("RAHDmicro01-RAHDmicro2", "RAHDMICRO1-RAHDMICRO2")
])
def test_standardize_label(input, expected_output):
    assert standardize_label(input) == expected_output
    return
