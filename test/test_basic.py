import pytest
import sys
sys.path.append("..")

from pywebmconverter.converter import *
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