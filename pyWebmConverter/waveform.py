"""
Audio waveform extraction and rendering for the video editor timeline.
"""
import array
import subprocess
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen
from .constants import WAVEFORM_BUCKETS, WAVEFORM_SAMPLE_RATE


def _extract_waveform(video_path: str, num_buckets: int, sample_rate: int) -> list:
    """Pipe mono PCM from ffmpeg and RMS-bucket into a normalised amplitude list."""
    try:
        proc = subprocess.run(
            [
                "ffmpeg", "-i", video_path,
                "-vn", "-ac", "1",
                "-ar", str(sample_rate),
                "-f", "f32le", "-",
            ],
            capture_output=True,
            check=False,
        )
        buf = array.array("f")
        buf.frombytes(proc.stdout)
    except (FileNotFoundError, OSError, ValueError):
        return []

    if not buf:
        return []

    chunk = max(1, len(buf) // num_buckets)
    result = []
    for i in range(num_buckets):
        slc = buf[i * chunk:(i + 1) * chunk]
        if slc:
            result.append((sum(x * x for x in slc) / len(slc)) ** 0.5)
    return result


class WaveformLoader(QThread):
    """Extracts audio waveform data from a video file without blocking the GUI."""

    waveform_ready = pyqtSignal(list)

    def __init__(self, video_path: str):
        super().__init__()
        self.video_path = video_path

    def run(self):
        """Extract waveform and emit the result."""
        amplitudes = _extract_waveform(self.video_path, WAVEFORM_BUCKETS, WAVEFORM_SAMPLE_RATE)
        self.waveform_ready.emit(amplitudes)


class WaveformWidget(QWidget):
    """
    Displays an audio waveform with a playhead and trim-region markers.
    Click or drag to seek to a position.
    """

    seek_requested = pyqtSignal(int)  # emits frame number

    _BG = QColor(20, 20, 20)
    _WAVE = QColor(70, 150, 190)
    _DIM = QColor(0, 0, 0, 120)
    _HEAD = QColor(255, 255, 255)
    _TRIM_START = QColor(80, 200, 100)
    _TRIM_END = QColor(210, 70, 70)

    def __init__(self, total_frames: int):
        super().__init__()
        self._amplitudes: list = []
        self._current_frame = 0
        self._start_frame = 0
        self._end_frame = max(0, total_frames - 1)
        self._total_frames = max(1, total_frames)
        self.setFixedHeight(60)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.SizeHorCursor)

    def set_waveform(self, amplitudes: list) -> None:
        """Load extracted amplitude data and repaint."""
        self._amplitudes = amplitudes
        self.update()

    def set_position(self, frame: int) -> None:
        """Move the playhead to the given frame and repaint."""
        self._current_frame = frame
        self.update()

    def set_trim(self, start: int, end: int) -> None:
        """Update the trim region markers and repaint."""
        self._start_frame = start
        self._end_frame = end
        self.update()

    def paintEvent(self, event):  # pylint: disable=unused-argument
        """Paint waveform bars, dim regions, trim markers, and playhead."""
        w, h = self.width(), self.height()
        mid = h // 2
        painter = QPainter(self)

        painter.fillRect(0, 0, w, h, self._BG)

        if self._amplitudes:
            mx = max(self._amplitudes) or 1.0
            n = len(self._amplitudes)
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._WAVE)
            for px in range(w):
                amp = self._amplitudes[int(px / w * n)] / mx
                half = max(1, int(amp * mid))
                painter.drawRect(px, mid - half, 1, half * 2)

        start_x = int(self._start_frame / self._total_frames * w)
        end_x = int(self._end_frame / self._total_frames * w)
        painter.fillRect(0, 0, start_x, h, self._DIM)
        painter.fillRect(end_x, 0, w - end_x, h, self._DIM)

        painter.setPen(QPen(self._TRIM_START, 2))
        painter.drawLine(start_x, 0, start_x, h)
        painter.setPen(QPen(self._TRIM_END, 2))
        painter.drawLine(end_x, 0, end_x, h)

        playhead_x = int(self._current_frame / self._total_frames * w)
        painter.setPen(QPen(self._HEAD, 1))
        painter.drawLine(playhead_x, 0, playhead_x, h)

        painter.end()

    def _frame_at(self, x: int) -> int:
        """Convert an x pixel coordinate to a frame number."""
        return max(0, min(self._total_frames - 1,
                          int(x / max(self.width(), 1) * self._total_frames)))

    def mousePressEvent(self, event):
        """Seek to the clicked position."""
        if event.button() == Qt.LeftButton:
            self.seek_requested.emit(self._frame_at(event.x()))

    def mouseMoveEvent(self, event):
        """Seek while dragging."""
        if event.buttons() & Qt.LeftButton:
            self.seek_requested.emit(self._frame_at(event.x()))
