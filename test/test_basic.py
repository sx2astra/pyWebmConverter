import pytest
import sys
import os

try:
    sys.path.append("pyWebmConverter")
    from converter import *
except ModuleNotFoundError:
    sys.path.insert(0, "/home/runner/work/pyWebmConverter/pyWebmConverter/pyWebMConverter")
    from converter import *
finally:
    pass

xfail = pytest.mark.xfail

def test_has_numbers():
    assert has_numbers("5") == True
    assert has_numbers("a") == False

@xfail(raises=ValueError)
def test_calculate_bitrate():
    assert WebmConverter.calculate_bitrate("", 10,10) == 8192
    assert WebmConverter.calculate_bitrate("", "10","10") == 8192
    assert WebmConverter.calculate_bitrate("", "a","b") == 8192

def test_set_file_name():
    assert WebmConverter.set_file_name("", "abc") == "abc.webm"
    assert WebmConverter.set_file_name("", "abc.webm") == "abc.webm"

if __name__ == 'test_basic()':
    test_basic()