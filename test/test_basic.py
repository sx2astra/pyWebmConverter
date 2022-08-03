import pytest
import sys
import os

try:
    sys.path.append("pyWebmConverter")
    from converter import *
except ModuleNotFoundError:
    print("Here")
    path = "./"
    print(os.listdir(path))
    sys.path.insert(0, "/pyWebMConverter")
    path = "./"
    print(os.listdir(path))
    from converter import *
else:
    print("There")
    sys.path.insert(0, "/home/runner/work/pyWebmConverter/pyWebmConverter")
    from converter import *
finally:
    pass

xfail = pytest.mark.xfail

def testHasNumbers():
    assert hasNumbers("5") == True
    assert hasNumbers("a") == False

@xfail(raises=ValueError)
def testCalculateBitrate():
    assert webMConverter.calculateBitrate(10,10) == 8192
    assert webMConverter.calculateBitrate("10","10") == 8192
    assert webMConverter.calculateBitrate("a","b") == 8192


def testSetFileName():
    assert webMConverter.setFileName("abc") == "abc.webm"
    assert webMConverter.setFileName("abc.webm") == "abc.webm"

if __name__ == 'test_pyWebMConverter()':
    test_pyWebMConverter()