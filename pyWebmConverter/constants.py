"""
Configuration constants for FFmpeg WebM Converter.
Centralized definitions for magic numbers, thresholds, and parameter values.
"""

# Video codec configuration
CODEC_VP9 = "libvpx-vp9"
CODEC_AV1 = "libaom-av1"

# Bitrate thresholds (in bits per second)
AV1_BITRATE_THRESHOLD = 800000  # Use AV1 only for >= 800 kbps
VP9_ULTRA_LOW_THRESHOLD = 150000  # < 150 kbps
VP9_VERY_LOW_THRESHOLD = 250000  # < 250 kbps
VP9_LOW_THRESHOLD = 350000  # < 350 kbps
VP9_MODERATE_THRESHOLD = 550000  # < 550 kbps
VP9_GOOD_THRESHOLD = 800000  # < 800 kbps

# File size thresholds for auto-scaling (in MB)
FILESIZE_TINY = 0.5  # < 0.5 MB
FILESIZE_VERY_SMALL = 2.0  # < 2.0 MB
FILESIZE_SMALL = 3.0  # < 3.0 MB
FILESIZE_MEDIUM = 5.0  # < 5.0 MB

# Auto-scaling factors
SCALE_FACTOR_TINY = 0.2  # 0.2x for files < 0.5 MB
SCALE_FACTOR_EXTREME = 0.25  # 0.25x for ultra-low bitrates
SCALE_FACTOR_AGGRESSIVE = 0.35  # 0.35x for very low bitrates
SCALE_FACTOR_MODERATE = 0.5  # 0.5x for low bitrates
SCALE_FACTOR_LIGHT = 0.75  # 0.75x for moderate bitrates
SCALE_FACTOR_NATIVE = 1.0  # No scaling

# Audio configuration
AUDIO_CODEC = "libopus"
AUDIO_INITIAL_BITRATE = 96  # kbps — binary search starting midpoint
AUDIO_DEFAULT_BITRATE = (
    96000  # bps budgeted for audio during video encode (matches above)
)
AUDIO_MIN_BITRATE_KBPS = 8  # binary search lower bound
AUDIO_MAX_BITRATE_KBPS = 128  # binary search upper bound — Opus at 128 is transparent
AUDIO_BITRATE_STEP = 4  # kbps — binary search stops when range < this

# Audio adjustment parameters
AUDIO_ADJUSTMENT_MAX_ATTEMPTS = 12  # binary search converges in ~log2(312/4) ≈ 7 steps
AUDIO_EXTRACTION_FORMAT = "libopus"

# Bitrate safety margins — reserve headroom for container overhead + rate control variance.
# Applied directly to the bit budget so encoder parameters stay correct.
SAFETY_MARGIN_LARGE = 0.98  # >= 8MB  : 2% reserve
SAFETY_MARGIN_MEDIUM = 0.97  # 4–8MB  : 3% reserve
SAFETY_MARGIN_SMALL = 0.96  # 2–4MB  : 4% reserve
SAFETY_MARGIN_TINY = 0.94  # < 2MB  : 6% reserve (container overhead is bigger %)

# Rate control settings
# maxrate == video_bitrate: the safety margin in the budget is what keeps us under,
# not an artificially suppressed peak rate. bufsize = 2x gives VP9 a proper VBV window.
MAXRATE_FACTOR_VP9 = 1.0
MAXRATE_FACTOR_AV1 = 1.0
VBV_BUFSIZE_MULTIPLIER = 2

# Quality parameters
VP9_PROFILE = 2
VP9_AUTO_ALT_REF = 1
VP9_ARNR_MAXFRAMES = 15
VP9_ARNR_STRENGTH = 0
VP9_AQ_MODE = 0
VP9_TILE_ROWS = 0
VP9_ENABLE_TPL = 1

AV1_TILE_ROWS = 0

# CPU usage (quality vs speed trade-off)
CPU_USED_2PASS = 0  # Best quality for 2-pass
CPU_USED_1PASS = 6  # Faster for 1-pass
AV1_CPU_USED_2PASS = 5
AV1_CPU_USED_1PASS = 8

# Video codec settings
PACING_MODE = "good"
FRAME_PARALLEL = 1
ROW_MT = 1

# Threading and performance
NUM_THREADS = 16

# Rotation settings
ROTATION_ANGLES = {
    0: None,
    90: "transpose=1",
    180: "transpose=1,transpose=1",
    270: "transpose=2",
}

# UI defaults
DEFAULT_FILE_SIZE_MB = 3.0
DEFAULT_AUDIO = "on"
DEFAULT_AUDIO_OPTIONS = ["on", "off"]
DEFAULT_SCALE_OPTIONS = [
    "Auto",
    "1080p",
    "720p",
    "480p",
    "2x",
    "1.5x",
    "1.25x",
    "1x",
    "0.75x",
    "0.5x",
    "0.25x",
]
DEFAULT_2PASS = True
DEFAULT_AV1 = False

# Video editor settings
VIDEO_EDITOR_WIDTH = 900
VIDEO_EDITOR_HEIGHT = 700
VIDEO_PREVIEW_WIDTH = 480
VIDEO_PREVIEW_MAX_FPS = 60  # cap preview playback; skips source frames to compensate
VIDEO_SEEK_DEBOUNCE_MS = 25  # slider settle time before issuing a cv2 seek

# Temporary file settings
TEMP_FILE_PREFIX = "temp__"
TEMP_LOG_FILES = ["ffmpeg2pass-0.log", "ffmpeg-mbtree.log", "ffmpeg-mbtree.log.mbtree"]

# Format settings
OUTPUT_FORMAT = "webm"
EXTRACTED_AUDIO_FILENAME = "extracted_audio.opus"

# Error messages
ERROR_NO_INPUT = "Error: Please select an input video file first."
ERROR_REQUIRED_FIELDS = "Error: Please fill in all required fields."
ERROR_INVALID_FILESIZE = "Error: Please enter a valid file size (e.g., 3.0)."
ERROR_FILESIZE_NEGATIVE = "Error: File size must be greater than 0."
ERROR_INVALID_OVERRIDE = "Error: Please enter a valid override size (e.g., 2.8)."
ERROR_OVERRIDE_NEGATIVE = "Error: Override size must be greater than 0."
ERROR_NO_DURATION = "Error: Could not determine video duration."
ERROR_FILESIZE_TOO_SMALL = "Error: File size too small for target bitrate with audio."
ERROR_FFMPEG_NOT_FOUND = (
    "Error: ffmpeg.exe not found."
    " Please ensure it is in the same directory or in your PATH."
)

# Success/Info messages
INFO_EXTRACTING_AUDIO = (
    "<span style='color:blue'>Extracting audio for fine-tuning...</span>"
)
INFO_AUDIO_ADJUSTMENT = (
    "<span style='color:blue'>Audio adjustment {}: {}kbps = {:.3f}MB</span>"
)
INFO_TARGET_HIT = (
    "<span style='color:green'>Target hit! {:.3f}MB with {}kbps audio</span>"
)
INFO_ENCODING_PASS = "<span style='color:blue'>Starting encoding pass {}...</span>"
INFO_PASS_FAILED = "<span style='color:red'>Pass {} failed!</span>"
INFO_ENCODING_COMPLETE = "<span style='color:green'>Video encoding complete!</span>"
INFO_AUDIO_ADJUSTMENT_START = (
    "<span style='color:blue'>Starting audio bitrate adjustment...</span>"
)
INFO_AUDIO_ADJUSTMENT_COMPLETE = (
    "<span style='color:green'>Audio adjustment complete!"
    " Final audio bitrate: {}kbps</span>"
)
INFO_FINAL_COMPLETE = "<span style='color:green'>Final conversion complete!</span>"
INFO_READY = "<span style='color:blue'>Ready for next conversion.</span>"
