"""
FFmpeg worker thread for running encoding operations without blocking the GUI.
"""

import re
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal
from .constants import INFO_ENCODING_PASS, INFO_PASS_FAILED

_PROGRESS_RE = re.compile(r'time=(\d+):(\d+):(\d+\.\d+)')


class FFmpegWorker(QThread):
    """
    Worker thread that runs ffmpeg commands in the background.
    Prevents GUI freezing during encoding operations.
    Supports both single-pass and two-pass encoding.
    """

    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, int)
    progress_signal = pyqtSignal(int)  # percentage 0-100

    def __init__(self, cmd: str, cmd_pass2: str = None, duration_s: float = None):
        """
        Args:
            cmd: FFmpeg command for pass 1 (or single-pass)
            cmd_pass2: Optional FFmpeg command for pass 2
            duration_s: Clip duration in seconds, used for progress calculation
        """
        super().__init__()
        self.cmd = cmd
        self.cmd_pass2 = cmd_pass2
        self.duration_s = duration_s
        self._proc = None

    def cancel(self):
        """Terminate the running ffmpeg process."""
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()

    def _emit_progress(self, line: str, pass_num: int) -> None:
        """Parse time= from an FFmpeg output line and emit a progress percentage."""
        if not self.duration_s:
            return
        match = _PROGRESS_RE.search(line)
        if not match:
            return
        elapsed = (
            float(match.group(1)) * 3600
            + float(match.group(2)) * 60
            + float(match.group(3))
        )
        raw_pct = min(elapsed / self.duration_s, 1.0)
        if self.cmd_pass2:
            pct = int((pass_num - 1) * 50 + raw_pct * 50)
        else:
            pct = int(raw_pct * 100)
        self.progress_signal.emit(pct)

    def run(self):
        """Execute the ffmpeg commands."""
        try:
            self.log_signal.emit(INFO_ENCODING_PASS.format(1))
            with subprocess.Popen(
                self.cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            ) as proc:
                self._proc = proc
                for line in proc.stdout:
                    self.log_signal.emit(line.rstrip())
                    self._emit_progress(line, 1)
                proc.wait()
            self._proc = None

            if proc.returncode != 0:
                self.log_signal.emit(INFO_PASS_FAILED.format(1))
                self.finished_signal.emit(False, proc.returncode)
                return

            if self.cmd_pass2:
                self.log_signal.emit(INFO_ENCODING_PASS.format(2))
                with subprocess.Popen(
                    self.cmd_pass2,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                ) as proc2:
                    self._proc = proc2
                    for line in proc2.stdout:
                        self.log_signal.emit(line.rstrip())
                        self._emit_progress(line, 2)
                    proc2.wait()
                self._proc = None

                if proc2.returncode != 0:
                    self.log_signal.emit(INFO_PASS_FAILED.format(2))
                    self.finished_signal.emit(False, proc2.returncode)
                    return

            self.progress_signal.emit(100)
            self.finished_signal.emit(True, 0)

        except FileNotFoundError:
            self.log_signal.emit(
                "<span style='color:red'>Error: ffmpeg.exe not found."
                " Please ensure it is in the same directory or in your PATH.</span>"
            )
            self.finished_signal.emit(False, -1)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.log_signal.emit(f"<span style='color:red'>Error: {e}</span>")
            self.finished_signal.emit(False, -1)
