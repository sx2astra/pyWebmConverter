"""
FFmpeg command building utilities for WebM encoding.
Handles command construction for both VP9 and AV1 codecs with 1-pass and 2-pass encoding.
"""

from .constants import (
    CODEC_VP9,
    CODEC_AV1,
    AV1_BITRATE_THRESHOLD,
    VP9_ULTRA_LOW_THRESHOLD,
    VP9_VERY_LOW_THRESHOLD,
    VP9_LOW_THRESHOLD,
    VP9_MODERATE_THRESHOLD,
    VP9_GOOD_THRESHOLD,
    FILESIZE_TINY,
    FILESIZE_VERY_SMALL,
    FILESIZE_SMALL,
    FILESIZE_MEDIUM,
    SCALE_FACTOR_TINY,
    SCALE_FACTOR_EXTREME,
    SCALE_FACTOR_AGGRESSIVE,
    SCALE_FACTOR_MODERATE,
    SCALE_FACTOR_LIGHT,
    SCALE_FACTOR_NATIVE,
    MAXRATE_FACTOR_VERYSMALL_VP9,
    MAXRATE_FACTOR_SMALL_VP9,
    MAXRATE_FACTOR_AV1,
    CPU_USED_2PASS,
    CPU_USED_1PASS,
    AV1_CPU_USED_2PASS,
    AV1_CPU_USED_1PASS,
    NUM_THREADS,
    PACING_MODE,
    FRAME_PARALLEL,
    ROW_MT,
    VP9_PROFILE,
    VP9_AUTO_ALT_REF,
    VP9_ARNR_MAXFRAMES,
    VP9_ARNR_STRENGTH,
    VP9_AQ_MODE,
    VP9_TILE_ROWS,
    VP9_ENABLE_TPL,
    AV1_TILE_ROWS,
    OUTPUT_FORMAT,
    ROTATION_ANGLES,
)


def select_codec_and_factors(
    file_size_mb: float, video_bitrate: int, allow_av1: bool
) -> tuple:
    """
    Select the best codec and rate control factors based on bitrate and file size.

    Args:
        file_size_mb: Target file size in MB
        video_bitrate: Video bitrate in bits per second
        allow_av1: Whether AV1 codec is allowed

    Returns:
        Tuple of (codec, cpu_used_2pass, cpu_used_1pass, tile_columns, maxrate_factor)
    """
    if allow_av1 and video_bitrate >= AV1_BITRATE_THRESHOLD:
        return (
            CODEC_AV1,
            AV1_CPU_USED_2PASS,
            AV1_CPU_USED_1PASS,
            2,
            MAXRATE_FACTOR_AV1,
        )

    # VP9 codec selection with adaptive rate control
    if file_size_mb < FILESIZE_MEDIUM:
        maxrate_factor = MAXRATE_FACTOR_VERYSMALL_VP9
    else:
        maxrate_factor = MAXRATE_FACTOR_SMALL_VP9

    return CODEC_VP9, CPU_USED_2PASS, CPU_USED_1PASS, 1, maxrate_factor


def get_auto_scale_factor(file_size_mb: float, video_bitrate: int) -> tuple[float, str]:
    """
    Calculate auto-scaling factor and message based on file size and bitrate.

    Args:
        file_size_mb: Target file size in MB
        video_bitrate: Video bitrate in bits per second

    Returns:
        Tuple of (scale_factor, description_message)
    """
    if file_size_mb < FILESIZE_TINY:
        return SCALE_FACTOR_TINY, "0.2x (tiny file, critical compression)"
    elif video_bitrate < VP9_ULTRA_LOW_THRESHOLD:
        return SCALE_FACTOR_EXTREME, "0.25x (extremely low bitrate)"
    elif (
        file_size_mb < FILESIZE_VERY_SMALL and video_bitrate < VP9_LOW_THRESHOLD
    ) or video_bitrate < VP9_VERY_LOW_THRESHOLD:
        return SCALE_FACTOR_AGGRESSIVE, "0.35x (small file/very low bitrate)"
    elif (
        file_size_mb < FILESIZE_SMALL and video_bitrate < VP9_MODERATE_THRESHOLD
    ) or video_bitrate < VP9_LOW_THRESHOLD:
        return SCALE_FACTOR_MODERATE, "0.5x (low bitrate)"
    elif (
        file_size_mb < FILESIZE_MEDIUM and video_bitrate < VP9_GOOD_THRESHOLD
    ) or video_bitrate < VP9_MODERATE_THRESHOLD:
        return SCALE_FACTOR_LIGHT, "0.75x (moderate bitrate)"

    return SCALE_FACTOR_NATIVE, "1.0x (adequate bitrate)"


def build_video_filters(
    scale_factor: float,
    user_scale_factor: float = 1.0,
    rotation: int = 0,
) -> str:
    """
    Build the video filter chain for scaling and rotation.

    Args:
        scale_factor: Auto-calculated scale factor
        user_scale_factor: User-provided scale factor from editor
        rotation: Rotation angle (0, 90, 180, 270)

    Returns:
        Comma-separated filter string
    """
    filters = []

    # Apply rotation if specified
    if rotation > 0:
        rotation_filter = ROTATION_ANGLES.get(rotation)
        if rotation_filter:
            filters.append(rotation_filter)

    # Apply scaling
    combined_scale_factor = scale_factor * user_scale_factor
    scale_filter = f"scale=iw*{combined_scale_factor}:ih*{combined_scale_factor}"
    filters.append(scale_filter)

    return ",".join(filters)


def build_vp9_quality_params(cpu_used: int) -> str:
    """
    Build VP9-specific quality parameters.

    Args:
        cpu_used: CPU usage level (0-16, higher = faster)

    Returns:
        Quality parameters string
    """
    return (
        f"-profile:v {VP9_PROFILE} "
        f"-cpu-used {cpu_used} "
        f"-auto-alt-ref {VP9_AUTO_ALT_REF} "
        f"-arnr-maxframes {VP9_ARNR_MAXFRAMES} "
        f"-arnr-strength {VP9_ARNR_STRENGTH} "
        f"-aq-mode {VP9_AQ_MODE} "
        f"-tile-rows {VP9_TILE_ROWS} "
        f"-tune-content default "
        f"-enable-tpl {VP9_ENABLE_TPL}"
    )


def build_av1_quality_params(cpu_used: int, tile_columns: int) -> str:
    """
    Build AV1-specific quality parameters.

    Args:
        cpu_used: CPU usage level
        tile_columns: Number of tile columns for parallelism

    Returns:
        Quality parameters string
    """
    return (
        f"-cpu-used {cpu_used} "
        f"-tile-rows {AV1_TILE_ROWS} "
        f"-tile-columns {tile_columns}"
    )


def build_base_command(
    input_video: str,
    codec: str,
    video_bitrate: int,
    maxrate: int,
    filters: str,
    quality_params: str,
    trim_prefix: str = "",
) -> str:
    """
    Build the base ffmpeg command (shared by 1-pass and 2-pass encoding).

    Args:
        input_video: Path to input video
        codec: Video codec (libvpx-vp9 or libaom-av1)
        video_bitrate: Target video bitrate
        maxrate: Maximum bitrate
        filters: Video filter chain
        quality_params: Codec-specific quality parameters
        trim_prefix: Optional trim parameters

    Returns:
        Base ffmpeg command string
    """
    undershoot = " -undershoot-pct 5" if codec == CODEC_VP9 else ""

    return (
        f"ffmpeg.exe -threads {NUM_THREADS} {trim_prefix}"
        f'-i "{input_video}" '
        f"-c:v {codec} "
        f"-pix_fmt yuv420p10le "
        f"-b:v {video_bitrate} "
        f"-maxrate {maxrate} "
        f"-bufsize {maxrate}{undershoot} "
        f"-deadline {PACING_MODE} "
        f"-frame-parallel {FRAME_PARALLEL} "
        f"-row-mt {ROW_MT} "
        f"{quality_params} "
        f"-vf {filters} "
    )


def build_audio_params(audio_enabled: bool, audio_bitrate: int = 0) -> str:
    """
    Build audio parameters for ffmpeg command.

    Args:
        audio_enabled: Whether audio is enabled
        audio_bitrate: Audio bitrate in bits per second

    Returns:
        Audio parameters string
    """
    if not audio_enabled:
        return "-an "
    return f"-c:a libopus -b:a {audio_bitrate} "


def build_encoding_commands(
    input_video: str,
    output_file: str,
    video_bitrate: int,
    audio_enabled: bool,
    audio_bitrate: int,
    codec: str,
    cpu_used_2pass: int,
    cpu_used_1pass: int,
    tile_columns: int,
    maxrate_factor: float,
    filters: str,
    use_2pass: bool,
    trim_prefix: str = "",
) -> tuple:
    """
    Build complete ffmpeg encoding commands for 1-pass or 2-pass encoding.

    Args:
        input_video: Path to input video
        output_file: Path to output file
        video_bitrate: Video bitrate
        audio_enabled: Whether to include audio
        audio_bitrate: Audio bitrate
        codec: Video codec
        cpu_used_2pass: CPU used setting for 2-pass
        cpu_used_1pass: CPU used setting for 1-pass
        tile_columns: Tile columns for parallelism
        maxrate_factor: Maxrate cap factor
        filters: Video filter chain
        use_2pass: Whether to use 2-pass encoding
        trim_prefix: Optional trim parameters

    Returns:
        Tuple of (command_pass1, command_pass2 or None)
    """
    maxrate = int(video_bitrate * maxrate_factor)
    cpu_used = cpu_used_2pass if use_2pass else cpu_used_1pass

    # Build quality parameters based on codec
    if codec == CODEC_VP9:
        quality_params = build_vp9_quality_params(cpu_used)
    else:
        quality_params = build_av1_quality_params(cpu_used, tile_columns)

    # Build base command
    base_cmd = build_base_command(
        input_video, codec, video_bitrate, maxrate, filters, quality_params, trim_prefix
    )

    audio_params = build_audio_params(audio_enabled, audio_bitrate)

    # Build pass commands
    if use_2pass:
        # Pass 1: No audio, only video
        cmd_pass1 = base_cmd + f"-pass 1 -f {OUTPUT_FORMAT} nul"
        # Pass 2: Add audio and output
        cmd_pass2 = (
            base_cmd + f"-pass 2 {audio_params}" + f'-f {OUTPUT_FORMAT} "{output_file}"'
        )
        return cmd_pass1, cmd_pass2

    # Single pass: Add audio and output
    cmd = base_cmd + audio_params + f'-f {OUTPUT_FORMAT} "{output_file}"'
    return cmd, None
