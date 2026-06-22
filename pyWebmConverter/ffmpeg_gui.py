"""
FFmpeg WebM Converter GUI

This is a simple graphical user interface (GUI) application built with PyQt5.
It allows users to convert video files to WebM format using the ffmpeg tool.
The GUI collects input details like file paths, scale, quality, and settings,
then runs ffmpeg in the background to perform the conversion.
"""

import sys
import subprocess
import re
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QTextEdit,
    QDialog,
    QCheckBox,
)
from PyQt5.QtCore import Qt

# Import from modular components
from .video_editor import VideoEditorDialog
from .ffmpeg_worker import FFmpegWorker
from .audio_processor import adjust_audio_bitrate
from .command_builder import (
    select_codec_and_factors,
    get_auto_scale_factor,
    build_video_filters,
    build_encoding_commands,
)
from .constants import (
    DEFAULT_FILE_SIZE_MB,
    DEFAULT_AUDIO,
    DEFAULT_AUDIO_OPTIONS,
    DEFAULT_SCALE_OPTIONS,
    DEFAULT_2PASS,
    DEFAULT_AV1,
    TEMP_LOG_FILES,
    ERROR_NO_INPUT,
    ERROR_REQUIRED_FIELDS,
    ERROR_INVALID_FILESIZE,
    ERROR_FILESIZE_NEGATIVE,
    ERROR_INVALID_OVERRIDE,
    ERROR_OVERRIDE_NEGATIVE,
    ERROR_NO_DURATION,
    ERROR_FILESIZE_TOO_SMALL,
    INFO_ENCODING_COMPLETE,
    INFO_AUDIO_ADJUSTMENT_START,
    INFO_AUDIO_ADJUSTMENT_COMPLETE,
    INFO_FINAL_COMPLETE,
    INFO_READY,
    AUDIO_DEFAULT_BITRATE,
    SAFETY_MARGIN_LARGE,
    SAFETY_MARGIN_MEDIUM,
    SAFETY_MARGIN_SMALL,
    SAFETY_MARGIN_TINY,
)


def _safety_margin(file_size_mb: float) -> float:
    if file_size_mb < 2.0:
        return SAFETY_MARGIN_TINY
    if file_size_mb < 4.0:
        return SAFETY_MARGIN_SMALL
    if file_size_mb < 8.0:
        return SAFETY_MARGIN_MEDIUM
    return SAFETY_MARGIN_LARGE


def get_video_duration(input_path: str) -> float:
    """
    Extract video duration using ffmpeg.

    Args:
        input_path: Path to the video file

    Returns:
        Duration in seconds, or None if unable to determine
    """
    cmd = ["ffmpeg", "-i", input_path]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    output = proc.stderr  # Duration info is in stderr
    match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", output)
    if match:
        h, m, s = map(float, match.groups())
        return h * 3600 + m * 60 + s
    return None


def get_video_dimensions(input_path: str) -> tuple:
    """
    Extract video dimensions (width, height) using ffprobe.

    Args:
        input_path: Path to the video file

    Returns:
        Tuple of (width, height), or (None, None) if unable to determine
    """
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height",
        "-of",
        "csv=p=0",
        input_path,
    ]
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
    except FileNotFoundError:
        return None, None
    output = proc.stdout.strip()
    if output:
        parts = output.split(",")
        if len(parts) >= 2:
            try:
                width = int(parts[0])
                height = int(parts[1])
                if width > 0 and height > 0:
                    return width, height
            except ValueError:
                pass
    return None, None


class FFmpegGUI(QWidget):
    """
    Main GUI window for WebM conversion.
    Provides input fields, conversion options, and real-time logging.
    """

    def __init__(self):
        """Initialize the GUI window."""
        super().__init__()
        # Store editor results
        self.editor_values = {
            "start_time": None,
            "duration": None,
            "rotation": 0,
        }
        self.init_ui()

    def init_ui(self):
        """Set up all UI elements."""
        self.setWindowTitle("FFmpeg WebM Converter")
        layout = QVBoxLayout()

        # Input video section
        self.input_label = QLabel("Input Video:")
        self.input_path = QLineEdit()
        self.input_browse = QPushButton("Browse")
        self.input_browse.clicked.connect(self.browse_input)
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_path)
        input_layout.addWidget(self.input_browse)
        layout.addWidget(self.input_label)
        layout.addLayout(input_layout)

        # Output directory section
        self.out_label = QLabel("Output Directory:")
        self.out_path = QLineEdit()
        self.out_browse = QPushButton("Browse")
        self.out_browse.clicked.connect(self.browse_output)
        out_layout = QHBoxLayout()
        out_layout.addWidget(self.out_path)
        out_layout.addWidget(self.out_browse)
        layout.addWidget(self.out_label)
        layout.addLayout(out_layout)

        # Output filename section
        self.file_label = QLabel("Output Filename:")
        self.file_name = QLineEdit()
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_name)

        # Edit video button
        self.edit_btn = QPushButton("Edit Video (Preview, Trim, Rotate, Scale)")
        self.edit_btn.clicked.connect(self.open_video_editor)
        layout.addWidget(self.edit_btn)

        # Scale section
        self.scale_label = QLabel("Scale:")
        self.scale_combo = QComboBox()
        self.scale_combo.addItems(DEFAULT_SCALE_OPTIONS)
        layout.addWidget(self.scale_label)
        layout.addWidget(self.scale_combo)

        # Target File Size section
        self.file_size_label = QLabel("Target File Size (MB):")
        self.file_size_input = QLineEdit()
        self.file_size_input.setPlaceholderText(
            "Enter target size (e.g., 3.0 for ~4MB, 8.0 for ~10MB)"
        )
        self.file_size_input.setText(str(DEFAULT_FILE_SIZE_MB))
        layout.addWidget(self.file_size_label)
        layout.addWidget(self.file_size_input)

        # Override target size for bitrate calculation (optional)
        self.override_label = QLabel(
            "Override Target Size for Bitrate (MB): (leave blank to use target size)"
        )
        self.override_input = QLineEdit()
        self.override_input.setPlaceholderText(
            "Optional: Use different size for bitrate calculation (e.g., 2.8 to reduce overshoot)"
        )
        layout.addWidget(self.override_label)
        layout.addWidget(self.override_input)

        # Audio section
        self.audio_label = QLabel("Audio:")
        self.audio_combo = QComboBox()
        self.audio_combo.addItems(DEFAULT_AUDIO_OPTIONS)
        layout.addWidget(self.audio_label)
        layout.addWidget(self.audio_combo)

        # AV1 codec support checkbox
        self.av1_checkbox = QCheckBox("Allow AV1 codec (for systems that support it)")
        self.av1_checkbox.setChecked(DEFAULT_AV1)
        layout.addWidget(self.av1_checkbox)

        # 2-Pass encoding checkbox
        self.twopass_checkbox = QCheckBox("2-Pass Encoding (higher quality, slower)")
        self.twopass_checkbox.setChecked(DEFAULT_2PASS)
        layout.addWidget(self.twopass_checkbox)

        # Start button
        self.start_btn = QPushButton("Start Conversion")
        self.start_btn.clicked.connect(self.start_conversion)
        layout.addWidget(self.start_btn)

        self.open_folder_btn = QPushButton("Open Output Folder")
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        self.open_folder_btn.setVisible(False)
        layout.addWidget(self.open_folder_btn)

        # Output log section
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.setLayout(layout)

    def browse_input(self):
        """Open file dialog to select input video."""
        fname, _ = QFileDialog.getOpenFileName(self, "Select Input Video")
        if fname:
            self.input_path.setText(fname)
            self.file_name.setText(os.path.splitext(os.path.basename(fname))[0])

    def browse_output(self):
        """Open folder dialog to select output directory."""
        folder = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if folder:
            self.out_path.setText(folder)

    def open_video_editor(self):
        """Open the video editor dialog for trimming, rotating, and scaling."""
        input_video = self.input_path.text().strip()
        if not input_video:
            self.log.append(f"<span style='color:red'>{ERROR_NO_INPUT}</span>")
            return

        # Open video editor dialog
        editor = VideoEditorDialog(input_video, self)
        if editor.exec_() == QDialog.Accepted:
            self.editor_values = editor.get_edit_values()
            start = self.editor_values["start_time"]
            dur = self.editor_values["duration"]
            rot = self.editor_values["rotation"]
            self.log.append(
                f"<span style='color:blue'>Video edited: Trim {start:.2f}s"
                f" for {dur:.2f}s, Rotation: {rot}°</span>"
            )
        editor.cap.release()

    def start_conversion(self):
        """Start the video conversion process."""
        # Get values from UI
        input_video = self.input_path.text().strip()
        out_dir = self.out_path.text().strip()
        file_name = self.file_name.text().strip()
        if file_name and not file_name.endswith(".webm"):
            file_name += ".webm"
        self.file_name.setText(file_name)
        scale = self.scale_combo.currentText()
        audio = self.audio_combo.currentText()

        # Validate required fields
        if not input_video or not out_dir or not file_name:
            self.log.append(f"<span style='color:red'>{ERROR_REQUIRED_FIELDS}</span>")
            return

        # Get and validate target file size
        try:
            file_size_mb = float(self.file_size_input.text().strip())
            if file_size_mb <= 0:
                self.log.append(
                    f"<span style='color:red'>{ERROR_FILESIZE_NEGATIVE}</span>"
                )
                return
        except ValueError:
            self.log.append(f"<span style='color:red'>{ERROR_INVALID_FILESIZE}</span>")
            return

        # Get and validate override target size (optional)
        override_size_mb = None
        override_text = self.override_input.text().strip()
        if override_text:
            try:
                override_size_mb = float(override_text)
                if override_size_mb <= 0:
                    self.log.append(
                        f"<span style='color:red'>{ERROR_OVERRIDE_NEGATIVE}</span>"
                    )
                    return
            except ValueError:
                self.log.append(
                    f"<span style='color:red'>{ERROR_INVALID_OVERRIDE}</span>"
                )
                return

        # Get video duration
        full_duration_s = get_video_duration(input_video)
        if full_duration_s is None:
            self.log.append(f"<span style='color:red'>{ERROR_NO_DURATION}</span>")
            return

        # Use trimmed duration if available
        if self.editor_values["start_time"] is not None:
            duration_s = self.editor_values["duration"]
            start_t = self.editor_values["start_time"]
            trim_t = self.editor_values["duration"]
            trim_prefix = f"-ss {start_t:.2f} -t {trim_t:.2f} "
        else:
            duration_s = full_duration_s
            trim_prefix = ""

        # Calculate bitrate from target file size.
        # Safety margin reserves headroom for WebM container overhead and VP9/AV1
        # rate control variance so the output reliably stays under the limit.
        bitrate_target_mb = (
            override_size_mb if override_size_mb is not None else file_size_mb
        )
        margin = _safety_margin(file_size_mb)
        total_bits = bitrate_target_mb * 8 * 1024 * 1024 * margin
        total_bitrate = int(total_bits // duration_s)

        # Audio setup
        if audio == "on":
            audio_bitrate = AUDIO_DEFAULT_BITRATE
            video_bitrate = total_bitrate - audio_bitrate
            if video_bitrate <= 0:
                self.log.append(
                    f"<span style='color:red'>{ERROR_FILESIZE_TOO_SMALL}</span>"
                )
                return
        else:
            audio_bitrate = 0
            video_bitrate = total_bitrate

        # Auto-select codec based on bitrate
        allow_av1 = self.av1_checkbox.isChecked()
        use_2pass = self.twopass_checkbox.isChecked()
        codec, cpu_used_2pass, cpu_used_1pass, tile_columns, maxrate_factor = (
            select_codec_and_factors(file_size_mb, video_bitrate, allow_av1)
        )

        # Parse scale and intelligently adjust
        res_target_height = (
            None  # set for resolution-based scaling ("480p", "720p", "1080p")
        )
        if scale == "Auto":
            factor, scale_desc = get_auto_scale_factor(file_size_mb, video_bitrate)
            self.log.append(
                f"<span style='color:blue'>Auto-scaling: {scale_desc}</span>"
            )
        elif scale.endswith("p"):
            # Resolution-based scaling (480p, 720p, 1080p)
            res_target_height = int(scale[:-1])
            width, height = get_video_dimensions(input_video)
            if width is None or height is None:
                self.log.append(
                    "<span style='color:red'>Could not determine video dimensions "
                    "(is ffprobe installed and on PATH?)</span>"
                )
                return
            factor = 1.0  # unused when res_target_height is set
            self.log.append(
                f"<span style='color:blue'>Scaling to {scale}: source {width}x{height}</span>"
            )
        else:
            # Percentage-based scaling (2x, 0.75x, etc.)
            factor = float(scale[:-1])

        # Build video filters
        filters = build_video_filters(
            factor,
            self.editor_values["rotation"],
            target_height=res_target_height,
        )

        # Build ffmpeg commands
        output_file = f"{out_dir}/{file_name}"
        title = os.path.splitext(file_name)[0]
        cmd, cmd_pass2 = build_encoding_commands(
            input_video,
            output_file,
            video_bitrate,
            audio == "on",
            audio_bitrate,
            codec,
            cpu_used_2pass,
            cpu_used_1pass,
            tile_columns,
            maxrate_factor,
            filters,
            use_2pass,
            trim_prefix,
            title,
        )

        encoding_mode = "2-Pass" if use_2pass else "1-Pass"
        maxrate_pct = int(maxrate_factor * 100)
        base_info = (
            f"<span style='color:blue'>Using {codec} ({encoding_mode}) | "
            f"Bitrate: {video_bitrate}bps | Maxrate cap: {maxrate_pct}% | "
            f"Target: {file_size_mb}MB"
        )
        if override_size_mb is not None:
            self.log.append(
                base_info + f" | Bitrate calc from: {override_size_mb}MB</span>"
            )
        else:
            self.log.append(base_info + "</span>")
        self.log.append(
            "<span style='color:blue'>"
            "Quality Focus: 10-bit encoding with detailed parameters.</span>"
        )
        self.log.append(f"Pass 1: {cmd}")
        if cmd_pass2:
            self.log.append(f"Pass 2: {cmd_pass2}")

        # Store for later use in on_conversion_finished
        self.current_output_file = output_file
        self.current_audio = audio
        self.current_target_size_mb = file_size_mb
        self.current_trim_prefix = trim_prefix
        self.current_input_video = input_video

        # Start conversion
        self.open_folder_btn.setVisible(False)
        self.start_btn.setEnabled(False)
        self.worker = FFmpegWorker(cmd, cmd_pass2)
        self.worker.log_signal.connect(self.log.append)
        self.worker.finished_signal.connect(self.on_conversion_finished)
        self.worker.start()

    def on_conversion_finished(self, success: bool, code: int):
        """
        Handle conversion completion.

        Args:
            success: Whether the conversion succeeded
            code: Exit code from ffmpeg
        """
        if success:
            self.log.append(
                f"<span style='color:green'>{INFO_ENCODING_COMPLETE}</span>"
            )

            # Adjust audio bitrate if audio is enabled
            if hasattr(self, "current_audio") and self.current_audio == "on":
                self.log.append(INFO_AUDIO_ADJUSTMENT_START)
                trim_prefix = getattr(self, "current_trim_prefix", "")
                final_audio_bitrate = adjust_audio_bitrate(
                    self.current_input_video,
                    self.current_output_file,
                    self.current_target_size_mb,
                    self.log.append,
                    trim_prefix,
                )
                self.log.append(
                    INFO_AUDIO_ADJUSTMENT_COMPLETE.format(final_audio_bitrate)
                )

            self.log.append(f"<span style='color:green'>{INFO_FINAL_COMPLETE}</span>")

            # Show file size summary
            final_size_mb = os.path.getsize(self.current_output_file) / (1024 * 1024)
            pct = (final_size_mb / self.current_target_size_mb) * 100
            summary_color = "green" if final_size_mb <= self.current_target_size_mb else "red"
            self.log.append(
                f"<span style='color:{summary_color}'>"
                f"Output: {final_size_mb:.2f} MB / {self.current_target_size_mb:.1f} MB"
                f" target ({pct:.1f}%)</span>"
            )
            self.open_folder_btn.setVisible(True)

            # Clean up temporary ffmpeg files
            for temp_file in TEMP_LOG_FILES:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except Exception as e:
                    self.log.append(
                        f"<span style='color:orange'>"
                        f"Warning: Could not delete {temp_file}: {e}</span>"
                    )

            # Reset input fields for next conversion
            self.input_path.clear()
            self.file_name.clear()
            # Reset editor values
            self.editor_values = {
                "start_time": None,
                "duration": None,
                "rotation": 0,
            }
            self.log.append(f"<span style='color:blue'>{INFO_READY}</span>")
        else:
            self.log.append(
                f"<span style='color:red'>ffmpeg exited with code {code}."
                " Check the log above for details.</span>"
            )
        self.start_btn.setEnabled(True)


    def open_output_folder(self):
        """Open the output directory in Windows Explorer."""
        output_dir = os.path.dirname(self.current_output_file)
        os.startfile(output_dir)


def main():
    """Entry point for the pyWebmConverter GUI application."""
    app = QApplication(sys.argv)
    gui = FFmpegGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
