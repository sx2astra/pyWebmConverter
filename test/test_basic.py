import sys
import pytest

try:
    # For running in CMD
    sys.path.append("pyWebmConverter")
    from converter import *
except ModuleNotFoundError:
    # For running in instance
    sys.path.insert(
        0, "/home/runner/work/pyWebmConverter/pyWebmConverter/pyWebMConverter"
    )
    from converter import *
finally:
    pass

xfail = pytest.mark.xfail

def test_has_numbers():
    assert has_numbers("5") == True
    assert has_numbers("a") == False


@xfail(raises=ValueError)
def test_calculate_bitrate():
    assert WebmConverter.calculate_bitrate("", 10, 10) == 8192
    assert WebmConverter.calculate_bitrate("", "10", "10") == 8192
    assert WebmConverter.calculate_bitrate("", "a", "b") == 8192


def test_set_file_name():
    assert WebmConverter.set_file_name("", "abc") == "abc.webm"
    assert WebmConverter.set_file_name("", "abc.webm") == "abc.webm"


def test_parse_config():
    assert WebmConverter.parse_config("", "low", "on") == (
        "-crf 20 -qmin 50 -qmax 100",
        "-c:a libopus",
    )
    assert WebmConverter.parse_config("", "low", "off") == (
        "-crf 20 -qmin 50 -qmax 100",
        "-an",
    )
    assert WebmConverter.parse_config("", "mid", "on") == (
        "-crf 15 -qmin 25 -qmax 75",
        "-c:a libopus",
    )
    assert WebmConverter.parse_config("", "mid", "off") == (
        "-crf 15 -qmin 25 -qmax 75",
        "-an",
    )
    assert WebmConverter.parse_config("", "high", "on") == (
        "-crf 10 -qmin 0 -qmax 50",
        "-c:a libopus",
    )
    assert WebmConverter.parse_config("", "high", "off") == (
        "-crf 10 -qmin 0 -qmax 50",
        "-an",
    )


if __name__ == "test_basic()":
    test_basic()