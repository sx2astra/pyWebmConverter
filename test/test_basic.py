"""
Unit tests for pyWebmConverter core functions.
Tests the command builder, constants, and utility functions.
"""

import sys
import pytest
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pyWebmConverter.command_builder import (
    select_codec_and_factors,
    get_auto_scale_factor,
)
from pyWebmConverter.constants import (
    CODEC_VP9,
    CODEC_AV1,
    AV1_BITRATE_THRESHOLD,
    DEFAULT_SCALE_OPTIONS,
    SCALE_FACTOR_LIGHT,
    SCALE_FACTOR_NATIVE,
)


class TestCodecSelection:
    """Test codec and factor selection logic."""

    def test_select_vp9_for_low_bitrate(self):
        """VP9 should be selected for low bitrates."""
        codec, _, _, _, _ = select_codec_and_factors(3.0, 500000, allow_av1=True)
        assert codec == CODEC_VP9

    def test_select_av1_for_high_bitrate(self):
        """AV1 should be selected for high bitrates when allowed."""
        codec, _, _, _, _ = select_codec_and_factors(5.0, 1000000, allow_av1=True)
        assert codec == CODEC_AV1

    def test_av1_disabled_forces_vp9(self):
        """VP9 should be used when AV1 is disabled."""
        codec, _, _, _, _ = select_codec_and_factors(5.0, 1000000, allow_av1=False)
        assert codec == CODEC_VP9


class TestAutoScaling:
    """Test automatic scaling factor calculation."""

    def test_tiny_file_aggressive_scaling(self):
        """Very small files should get aggressive scaling."""
        scale_factor, message = get_auto_scale_factor(0.3, 100000)
        assert scale_factor < SCALE_FACTOR_LIGHT
        assert "critical compression" in message.lower() or "tiny" in message.lower()

    def test_medium_file_native_scaling(self):
        """Medium files can use native resolution."""
        scale_factor, message = get_auto_scale_factor(5.0, 500000)
        assert scale_factor >= SCALE_FACTOR_LIGHT

    def test_low_bitrate_scaling(self):
        """Low bitrates should trigger scaling reduction."""
        scale_factor, message = get_auto_scale_factor(3.0, 150000)
        assert scale_factor < SCALE_FACTOR_NATIVE
        assert "low bitrate" in message.lower() or "extreme" in message.lower()


class TestConstants:
    """Test configuration constants."""

    def test_scale_options_available(self):
        """Default scale options should be available."""
        assert len(DEFAULT_SCALE_OPTIONS) > 0
        assert "1x" in DEFAULT_SCALE_OPTIONS
        assert "0.5x" in DEFAULT_SCALE_OPTIONS

    def test_av1_bitrate_threshold_valid(self):
        """AV1 bitrate threshold should be reasonable."""
        assert AV1_BITRATE_THRESHOLD > 0
        assert AV1_BITRATE_THRESHOLD < 2000000  # Reasonable upper bound


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


if __name__ == "test_basic()":
    test_basic()
