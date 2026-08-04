"""
Unit tests for pyWebmConverter core functions.
Tests the command builder, constants, and utility functions.
"""
# pylint: disable=missing-function-docstring
from pyWebmConverter.command_builder import (
    select_codec_and_factors,
    get_auto_scale_factor,
    build_video_filters,
    build_encoding_commands,
    build_h264_encoding_commands,
)
from pyWebmConverter.constants import (
    CODEC_VP9,
    CODEC_AV1,
    AV1_BITRATE_THRESHOLD,
    SAFETY_MARGIN_LARGE,
    SAFETY_MARGIN_MEDIUM,
    SAFETY_MARGIN_SMALL,
    SAFETY_MARGIN_TINY,
)


# --- select_codec_and_factors ---

def test_codec_vp9_when_av1_disabled():
    codec, *_ = select_codec_and_factors(1_000_000, allow_av1=False)
    assert codec == CODEC_VP9


def test_codec_vp9_when_bitrate_below_av1_threshold():
    codec, *_ = select_codec_and_factors(AV1_BITRATE_THRESHOLD - 1, allow_av1=True)
    assert codec == CODEC_VP9


def test_codec_av1_when_enabled_and_bitrate_sufficient():
    codec, *_ = select_codec_and_factors(AV1_BITRATE_THRESHOLD, allow_av1=True)
    assert codec == CODEC_AV1


# --- get_auto_scale_factor ---

def test_auto_scale_tiny_file():
    factor, desc = get_auto_scale_factor(0.3, 500_000)
    assert factor == 0.2
    assert "tiny" in desc.lower()


def test_auto_scale_native_high_bitrate():
    factor, desc = get_auto_scale_factor(10.0, 2_000_000)
    assert factor == 1.0
    assert "1.0x" in desc


def test_auto_scale_4k_source_downscales_to_720p():
    # 10 MB / 45 s → ~1.73 Mbps video bitrate: fine for 720p, terrible for 4K
    factor, desc = get_auto_scale_factor(10.0, 1_730_000, source_height=2160)
    assert factor < 1.0
    assert "720" in desc


def test_auto_scale_source_already_small_stays_native():
    # 720p source at 1.73 Mbps should not downscale further
    factor, desc = get_auto_scale_factor(10.0, 1_730_000, source_height=720)
    assert factor == 1.0
    assert "1.0x" in desc


def test_auto_scale_returns_float():
    factor, desc = get_auto_scale_factor(3.0, 400_000)
    assert isinstance(factor, float)
    assert isinstance(desc, str)


# --- build_video_filters ---

def test_filters_scale_only():
    result = build_video_filters(0.5)
    assert "scale=iw*0.5:ih*0.5" in result
    assert "crop" not in result
    assert "transpose" not in result


def test_filters_with_rotation_90():
    result = build_video_filters(1.0, rotation=90)
    assert "transpose=1" in result


def test_filters_with_rotation_none():
    result = build_video_filters(1.0, rotation=0)
    assert "transpose" not in result


def test_filters_with_crop():
    result = build_video_filters(1.0, crop=(10, 20, 640, 360))
    assert result.startswith("crop=640:360:10:20")


def test_filters_crop_before_rotation():
    result = build_video_filters(1.0, rotation=90, crop=(0, 0, 100, 100))
    parts = result.split(",")
    assert parts[0].startswith("crop=")
    assert any("transpose" in p for p in parts[1:])


def test_filters_target_height():
    result = build_video_filters(1.0, target_height=720)
    assert "scale=-2:720" in result
    assert "iw*" not in result


def test_filters_fps_appended():
    result = build_video_filters(1.0, fps=30)
    assert result.endswith("fps=30")


def test_filters_fps_none_omitted():
    result = build_video_filters(1.0, fps=None)
    assert "fps" not in result


def test_filters_fps_after_scale():
    result = build_video_filters(0.5, fps=24)
    parts = result.split(",")
    scale_idx = next(i for i, p in enumerate(parts) if "scale" in p)
    fps_idx = next(i for i, p in enumerate(parts) if "fps" in p)
    assert fps_idx > scale_idx


# --- build_encoding_commands ---

def test_build_1pass_returns_none_for_pass2():
    cmd, cmd2 = build_encoding_commands(
        "in.mp4", "out.webm", 500_000, False, 0,
        CODEC_VP9, 0, 6, 1, 1.0, "scale=iw*1.0:ih*1.0", use_2pass=False,
    )
    assert cmd2 is None
    assert "out.webm" in cmd


def test_build_2pass_returns_both_commands():
    cmd1, cmd2 = build_encoding_commands(
        "in.mp4", "out.webm", 500_000, False, 0,
        CODEC_VP9, 0, 6, 1, 1.0, "scale=iw*1.0:ih*1.0", use_2pass=True,
    )
    assert cmd1 is not None
    assert cmd2 is not None
    assert "-pass 1" in cmd1
    assert "-pass 2" in cmd2


def test_build_command_includes_audio():
    cmd, _ = build_encoding_commands(
        "in.mp4", "out.webm", 500_000, True, 96_000,
        CODEC_VP9, 0, 6, 1, 1.0, "scale=iw*1.0:ih*1.0", use_2pass=False,
    )
    assert "libopus" in cmd
    assert "96000" in cmd


def test_build_command_no_audio():
    cmd, _ = build_encoding_commands(
        "in.mp4", "out.webm", 500_000, False, 0,
        CODEC_VP9, 0, 6, 1, 1.0, "scale=iw*1.0:ih*1.0", use_2pass=False,
    )
    assert "-an" in cmd
    assert "libopus" not in cmd


def test_build_command_metadata_title():
    cmd, _ = build_encoding_commands(
        "in.mp4", "out.webm", 500_000, False, 0,
        CODEC_VP9, 0, 6, 1, 1.0, "scale=iw*1.0:ih*1.0", use_2pass=False,
        title="myvideo",
    )
    assert 'title="myvideo"' in cmd


# --- build_h264_encoding_commands ---

def test_h264_1pass_uses_libx264():
    cmd, _ = build_h264_encoding_commands(
        "in.mp4", "out.mp4", 500_000, False, 0,
        "scale=iw*1.0:ih*1.0", use_2pass=False,
    )
    assert "libx264" in cmd


def test_h264_1pass_no_pass2():
    _, cmd2 = build_h264_encoding_commands(
        "in.mp4", "out.mp4", 500_000, False, 0,
        "scale=iw*1.0:ih*1.0", use_2pass=False,
    )
    assert cmd2 is None


def test_h264_2pass_returns_both():
    cmd1, cmd2 = build_h264_encoding_commands(
        "in.mp4", "out.mp4", 500_000, False, 0,
        "scale=iw*1.0:ih*1.0", use_2pass=True,
    )
    assert "-pass 1" in cmd1
    assert "-pass 2" in cmd2


def test_h264_pass1_uses_null_muxer():
    cmd1, _ = build_h264_encoding_commands(
        "in.mp4", "out.mp4", 500_000, False, 0,
        "scale=iw*1.0:ih*1.0", use_2pass=True,
    )
    assert "-f null" in cmd1


def test_h264_output_uses_mp4_format():
    _, cmd2 = build_h264_encoding_commands(
        "in.mp4", "out.mp4", 500_000, False, 0,
        "scale=iw*1.0:ih*1.0", use_2pass=True,
    )
    assert "-f mp4" in cmd2


def test_h264_audio_uses_aac():
    cmd, _ = build_h264_encoding_commands(
        "in.mp4", "out.mp4", 500_000, True, 128_000,
        "scale=iw*1.0:ih*1.0", use_2pass=False,
    )
    assert "aac" in cmd
    assert "libopus" not in cmd


def test_h264_yuv420p_not_10bit():
    cmd, _ = build_h264_encoding_commands(
        "in.mp4", "out.mp4", 500_000, False, 0,
        "scale=iw*1.0:ih*1.0", use_2pass=False,
    )
    assert "yuv420p" in cmd
    assert "yuv420p10" not in cmd


def test_h264_movflags_faststart():
    cmd, _ = build_h264_encoding_commands(
        "in.mp4", "out.mp4", 500_000, False, 0,
        "scale=iw*1.0:ih*1.0", use_2pass=False,
    )
    assert "faststart" in cmd


# --- safety margin ordering ---

def test_safety_margins_ordered():
    """Larger files get a looser margin (closer to 1.0)."""
    assert SAFETY_MARGIN_TINY < SAFETY_MARGIN_SMALL
    assert SAFETY_MARGIN_SMALL < SAFETY_MARGIN_MEDIUM
    assert SAFETY_MARGIN_MEDIUM < SAFETY_MARGIN_LARGE
    assert SAFETY_MARGIN_LARGE <= 1.0
