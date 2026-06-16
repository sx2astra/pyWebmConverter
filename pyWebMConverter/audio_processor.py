"""
Audio processing utilities for fine-tuning audio bitrate to match target file size.
"""

import os
import subprocess
from .constants import (
    AUDIO_INITIAL_BITRATE,
    AUDIO_BITRATE_STEP,
    AUDIO_ADJUSTMENT_MAX_ATTEMPTS,
    AUDIO_ADJUSTMENT_TOLERANCE_MB,
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
    lower_tolerance_mb: float = AUDIO_ADJUSTMENT_TOLERANCE_MB,
) -> int:
    """
    Iteratively adjusts audio bitrate to hit the target file size precisely.

    Args:
        original_video: Path to the original video file
        encoded_video: Path to the encoded video (with video already encoded)
        target_size_mb: Target file size in MB
        log_callback: Callback function to log messages
        trim_prefix: Optional ffmpeg trim parameters (-ss and -t)
        lower_tolerance_mb: Tolerance in MB below target

    Returns:
        Final audio bitrate used (in kbps)
    """
    target_size_bytes = target_size_mb * 1024 * 1024
    lower_tolerance_bytes = lower_tolerance_mb * 1024 * 1024
    current_audio_bitrate_kbps = AUDIO_INITIAL_BITRATE
    extracted_audio = EXTRACTED_AUDIO_FILENAME

    # Get the directory of the output file
    output_dir = os.path.dirname(encoded_video) or "."

    # Extract audio from the original video (with trim parameters applied)
    log_callback(INFO_EXTRACTING_AUDIO)
    extracted_audio_path = os.path.join(output_dir, extracted_audio)

    # Apply trim parameters to audio extraction if trim_prefix is provided
    extract_cmd = f'ffmpeg.exe -y {trim_prefix}-i "{original_video}" -vn -c:a {AUDIO_EXTRACTION_FORMAT} "{extracted_audio_path}"'
    os.system(extract_cmd)

    for attempt in range(AUDIO_ADJUSTMENT_MAX_ATTEMPTS):
        # Re-encode audio with current bitrate and mux with video
        # Create temp file in SAME directory as output to avoid cross-drive issues
        temp_output = os.path.join(
            output_dir, f"{TEMP_FILE_PREFIX}{os.path.basename(encoded_video)}"
        )
        cmd_adjust_audio = f'ffmpeg.exe -y -i "{encoded_video}" -i "{extracted_audio_path}" -c:v copy -c:a libopus -b:a {current_audio_bitrate_kbps}k -map 0:v:0 -map 1:a:0 "{temp_output}"'
        os.system(cmd_adjust_audio)

        current_size_bytes = os.path.getsize(temp_output)
        log_callback(
            INFO_AUDIO_ADJUSTMENT.format(
                attempt + 1,
                current_audio_bitrate_kbps,
                current_size_bytes / (1024 * 1024),
            )
        )

        # Check if within tolerance
        if current_size_bytes <= target_size_bytes and current_size_bytes >= (
            target_size_bytes - lower_tolerance_bytes
        ):
            log_callback(
                INFO_TARGET_HIT.format(
                    current_size_bytes / (1024 * 1024), current_audio_bitrate_kbps
                )
            )
            os.replace(temp_output, encoded_video)
            break

        # Adjust bitrate
        if current_size_bytes > target_size_bytes:
            current_audio_bitrate_kbps -= AUDIO_BITRATE_STEP
        else:
            current_audio_bitrate_kbps += AUDIO_BITRATE_STEP

        os.replace(temp_output, encoded_video)

    # Clean up extracted audio
    try:
        os.remove(extracted_audio_path)
    except Exception:
        pass

    return current_audio_bitrate_kbps
