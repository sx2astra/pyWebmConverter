"""
Audio processing utilities for fine-tuning audio bitrate to match target file size.
"""

import os
from .constants import (
    AUDIO_INITIAL_BITRATE,
    AUDIO_MIN_BITRATE_KBPS,
    AUDIO_MAX_BITRATE_KBPS,
    AUDIO_BITRATE_STEP,
    AUDIO_ADJUSTMENT_MAX_ATTEMPTS,
    AUDIO_EXTRACTION_FORMAT,
    EXTRACTED_AUDIO_FILENAME,
    TEMP_FILE_PREFIX,
    INFO_EXTRACTING_AUDIO,
    INFO_AUDIO_ADJUSTMENT,
    INFO_TARGET_HIT,
)


def adjust_audio_bitrate(
    original_video: str,
    encoded_video: str,
    target_size_mb: float,
    log_callback,
    trim_prefix: str = "",
) -> int:
    """
    Binary-search for the highest audio bitrate that keeps the file under target.

    Replaces encoded_video in-place each time a better (higher kbps, still
    under target) candidate is found. If no candidate fits, encoded_video is
    left unchanged (initial 96 kbps audio from the main encode).

    Args:
        original_video: Path to the original video file
        encoded_video: Path to the already video-encoded output file
        target_size_mb: Hard upper limit in MB — must not exceed this
        log_callback: Function to send log strings to the GUI
        trim_prefix: Optional ffmpeg trim flags (-ss / -t)

    Returns:
        Final audio bitrate used in kbps
    """
    target_size_bytes = target_size_mb * 1024 * 1024
    output_dir = os.path.dirname(encoded_video) or "."
    extracted_audio_path = os.path.join(output_dir, EXTRACTED_AUDIO_FILENAME)
    temp_output = os.path.join(
        output_dir, f"{TEMP_FILE_PREFIX}{os.path.basename(encoded_video)}"
    )

    log_callback(INFO_EXTRACTING_AUDIO)
    extract_cmd = (
        f'ffmpeg.exe -y {trim_prefix}-i "{original_video}"'
        f' -vn -c:a {AUDIO_EXTRACTION_FORMAT} "{extracted_audio_path}"'
    )
    os.system(extract_cmd)

    low = AUDIO_MIN_BITRATE_KBPS
    high = AUDIO_MAX_BITRATE_KBPS
    best_kbps = None  # highest kbps confirmed under target

    for attempt in range(AUDIO_ADJUSTMENT_MAX_ATTEMPTS):
        if high - low < AUDIO_BITRATE_STEP:
            break

        mid = (low + high) // 2

        cmd_adjust_audio = (
            f'ffmpeg.exe -y -i "{encoded_video}" -i "{extracted_audio_path}"'
            f' -c:v copy -c:a libopus -b:a {mid}k'
            f' -map 0:v:0 -map 1:a:0 "{temp_output}"'
        )
        os.system(cmd_adjust_audio)

        current_size_bytes = os.path.getsize(temp_output)
        log_callback(
            INFO_AUDIO_ADJUSTMENT.format(
                attempt + 1, mid, current_size_bytes / (1024 * 1024)
            )
        )

        if current_size_bytes <= target_size_bytes:
            # Under target — keep this result, search higher
            best_kbps = mid
            os.replace(temp_output, encoded_video)
            low = mid + AUDIO_BITRATE_STEP
        else:
            # Over target — discard and search lower
            try:
                os.remove(temp_output)
            except OSError:
                pass
            high = mid - AUDIO_BITRATE_STEP

    if best_kbps is not None:
        final_size_mb = os.path.getsize(encoded_video) / (1024 * 1024)
        log_callback(INFO_TARGET_HIT.format(final_size_mb, best_kbps))

    try:
        os.remove(extracted_audio_path)
    except OSError:
        pass

    return best_kbps if best_kbps is not None else AUDIO_INITIAL_BITRATE
