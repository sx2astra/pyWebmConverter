"""
FFmpeg worker thread for running encoding operations without blocking the GUI.
"""

import subprocess
from PyQt5.QtCore import QThread, pyqtSignal
from .constants import INFO_ENCODING_PASS, INFO_PASS_FAILED


class FFmpegWorker(QThread):
    """
    Worker thread that runs ffmpeg commands in the background.
    Prevents GUI freezing during encoding operations.
    Supports both single-pass and two-pass encoding.
    """

    log_signal = pyqtSignal(str)  # Signal to send log messages to the GUI
    finished_signal = pyqtSignal(bool, int)  # Signal when done (success, exit_code)

    def __init__(self, cmd: str, cmd_pass2: str = None):
        """
        Initialize the worker thread.

        Args:
            cmd: FFmpeg command for pass 1 (or single-pass)
            cmd_pass2: Optional FFmpeg command for pass 2 (if 2-pass encoding)
        """
        super().__init__()
        self.cmd = cmd
        self.cmd_pass2 = cmd_pass2

    def run(self):
        """Execute the ffmpeg commands."""
        try:
            # Pass 1 (or single-pass)
            self.log_signal.emit(INFO_ENCODING_PASS.format(1))
            proc = subprocess.Popen(
                self.cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )
            for line in proc.stdout:
                self.log_signal.emit(line.rstrip())
            proc.wait()

            if proc.returncode != 0:
                self.log_signal.emit(INFO_PASS_FAILED.format(1))
                self.finished_signal.emit(False, proc.returncode)
                return

            # Pass 2 if enabled
            if self.cmd_pass2:
                self.log_signal.emit(INFO_ENCODING_PASS.format(2))
                proc2 = subprocess.Popen(
                    self.cmd_pass2,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                )
                for line in proc2.stdout:
                    self.log_signal.emit(line.rstrip())
                proc2.wait()

                if proc2.returncode != 0:
                    self.log_signal.emit(INFO_PASS_FAILED.format(2))
                    self.finished_signal.emit(False, proc2.returncode)
                    return

            self.finished_signal.emit(True, 0)

        except FileNotFoundError:
            self.log_signal.emit(
                "<span style='color:red'>Error: ffmpeg.exe not found."
                " Please ensure it is in the same directory or in your PATH.</span>"
            )
            self.finished_signal.emit(False, -1)
        except Exception as e:
            self.log_signal.emit(f"<span style='color:red'>Error: {e}</span>")
            self.finished_signal.emit(False, -1)
