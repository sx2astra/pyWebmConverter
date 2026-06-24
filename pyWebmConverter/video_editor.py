"""
Video editor dialog for trimming, rotating, cropping, and previewing videos.
"""

import cv2
from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QSlider,
    QSpinBox,
    QComboBox,
    QSizePolicy,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, QTimer, QRect, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from .constants import (
    VIDEO_EDITOR_WIDTH,
    VIDEO_EDITOR_HEIGHT,
    VIDEO_PREVIEW_WIDTH,
    VIDEO_PREVIEW_MAX_FPS,
    VIDEO_SEEK_DEBOUNCE_MS,
)


class CropLabel(QLabel):
    """
    QLabel subclass that lets the user drag a crop rectangle over the video preview.
    Emits crop_changed with a QRect in display coordinates, or None when cleared.
    """

    crop_changed = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._start = None
        self._rect = None

    def mousePressEvent(self, event):
        """Begin a new crop selection on left-click."""
        if event.button() == Qt.LeftButton:
            self._start = event.pos()
            self._rect = None
            self.update()

    def mouseMoveEvent(self, event):
        """Extend the crop rectangle while the button is held."""
        if event.buttons() & Qt.LeftButton and self._start is not None:
            self._rect = QRect(self._start, event.pos()).normalized()
            self.update()

    def mouseReleaseEvent(self, event):
        """Finalise the crop rectangle and emit crop_changed."""
        if event.button() == Qt.LeftButton and self._start is not None:
            self._rect = QRect(self._start, event.pos()).normalized()
            self._start = None
            self.update()
            self.crop_changed.emit(self._rect)

    def clear_crop(self):
        """Remove the current crop selection."""
        self._rect = None
        self._start = None
        self.update()
        self.crop_changed.emit(None)

    def paintEvent(self, event):
        """Draw the crop overlay on top of the video frame."""
        super().paintEvent(event)
        if self._rect and not self._rect.isEmpty():
            painter = QPainter(self)
            painter.setPen(QPen(Qt.yellow, 2, Qt.DashLine))
            painter.drawRect(self._rect)
            painter.end()


class VideoEditorDialog(QDialog):
    """
    A separate dialog for video preview and editing.
    Allows users to trim, rotate, and crop video clips.
    """

    def __init__(self, video_path, parent=None, initial_values=None):
        super().__init__(parent)
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.orig_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.orig_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.current_frame = 0
        self.is_playing = False

        self.start_frame = 0
        self.end_frame = self.total_frames - 1
        self.rotation = 0
        self.crop = None  # (x, y, w, h) in original video pixels
        self._render_w = VIDEO_PREVIEW_WIDTH  # actual rendered pixmap width (updated each frame)
        self._render_h = 0

        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.play_video)

        # Debounce slider seeking — avoids hammering the decoder on every drag pixel
        self._pending_frame = 0
        self._seek_timer = QTimer()
        self._seek_timer.setSingleShot(True)
        self._seek_timer.timeout.connect(self._seek_to_pending)

        self._frames_per_tick = 1  # updated in toggle_play based on source fps

        self.init_ui()
        if initial_values:
            self._restore_values(initial_values)
        self.update_frame()

    def init_ui(self):
        """Set up the editor UI."""
        self.setWindowTitle("Video Editor")
        self.setGeometry(100, 100, VIDEO_EDITOR_WIDTH, VIDEO_EDITOR_HEIGHT)
        layout = QVBoxLayout()

        # Video display
        self.video_label = CropLabel()
        self.video_label.setMinimumSize(VIDEO_PREVIEW_WIDTH, 240)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background-color: black;")
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_label.crop_changed.connect(self.on_crop_changed)
        layout.addWidget(self.video_label, stretch=1)

        # Timeline slider
        timeline_layout = QHBoxLayout()
        timeline_layout.addWidget(QLabel("Timeline:"))
        self.timeline = QSlider(Qt.Horizontal)
        self.timeline.setMinimum(0)
        self.timeline.setMaximum(self.total_frames - 1)
        self.timeline.sliderMoved.connect(self.on_timeline_moved)
        self.timeline.setTracking(False)
        timeline_layout.addWidget(self.timeline)
        self.frame_label = QLabel(f"0/{self.total_frames}")
        timeline_layout.addWidget(self.frame_label)
        layout.addLayout(timeline_layout)

        # Playback controls
        playback_layout = QHBoxLayout()
        prev_btn = QPushButton("← Frame")
        prev_btn.clicked.connect(self.prev_frame)
        playback_layout.addWidget(prev_btn)
        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self.toggle_play)
        playback_layout.addWidget(self.play_btn)
        next_btn = QPushButton("Frame →")
        next_btn.clicked.connect(self.next_frame)
        playback_layout.addWidget(next_btn)
        layout.addLayout(playback_layout)

        # Trim section
        trim_layout = QHBoxLayout()
        trim_layout.addWidget(QLabel("Trim Start (frame):"))
        self.trim_start = QSpinBox()
        self.trim_start.setMinimum(0)
        self.trim_start.setMaximum(self.total_frames - 1)
        self.trim_start.valueChanged.connect(self.on_trim_changed)
        trim_layout.addWidget(self.trim_start)
        set_start_btn = QPushButton("Set Start")
        set_start_btn.clicked.connect(self.set_start_frame)
        trim_layout.addWidget(set_start_btn)

        trim_layout.addWidget(QLabel("Trim End (frame):"))
        self.trim_end = QSpinBox()
        self.trim_end.setMinimum(0)
        self.trim_end.setMaximum(self.total_frames - 1)
        self.trim_end.setValue(self.total_frames - 1)
        self.trim_end.valueChanged.connect(self.on_trim_changed)
        trim_layout.addWidget(self.trim_end)
        set_end_btn = QPushButton("Set End")
        set_end_btn.clicked.connect(self.set_end_frame)
        trim_layout.addWidget(set_end_btn)
        layout.addLayout(trim_layout)

        # Crop section
        crop_layout = QHBoxLayout()
        crop_layout.addWidget(QLabel("Crop:"))
        self.crop_info_label = QLabel("None — drag on the preview to set a crop region")
        crop_layout.addWidget(self.crop_info_label)
        crop_layout.addStretch()
        clear_crop_btn = QPushButton("Clear Crop")
        clear_crop_btn.clicked.connect(self.video_label.clear_crop)
        crop_layout.addWidget(clear_crop_btn)
        layout.addLayout(crop_layout)

        # Rotation section
        rotation_layout = QHBoxLayout()
        rotation_layout.addWidget(QLabel("Rotation:"))
        self.rotation_combo = QComboBox()
        self.rotation_combo.addItems(["0°", "90°", "180°", "270°"])
        self.rotation_combo.currentIndexChanged.connect(self.on_rotation_changed)
        rotation_layout.addWidget(self.rotation_combo)
        layout.addLayout(rotation_layout)

        # Buttons
        button_layout = QHBoxLayout()
        apply_btn = QPushButton("Apply & Close")
        apply_btn.clicked.connect(self.apply_and_close)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_frame(self):
        """Update the displayed video frame with transformations."""
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        ret, frame = self.cap.read()

        if ret:
            if self.rotation == 90:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            elif self.rotation == 180:
                frame = cv2.rotate(frame, cv2.ROTATE_180)
            elif self.rotation == 270:
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            src_h, src_w = frame_rgb.shape[:2]
            label_w = max(self.video_label.width(), VIDEO_PREVIEW_WIDTH)
            label_h = max(self.video_label.height(), 240)
            scale = min(label_w / src_w, label_h / src_h)
            preview_w = max(1, int(src_w * scale))
            preview_h = max(1, int(src_h * scale))
            self._render_w = preview_w
            self._render_h = preview_h
            frame_small = cv2.resize(
                frame_rgb, (preview_w, preview_h), interpolation=cv2.INTER_AREA
            )
            ph, pw, ch = frame_small.shape
            qt_image = QImage(frame_small.data, pw, ph, ch * pw, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qt_image))

            self.timeline.blockSignals(True)
            self.timeline.setValue(self.current_frame)
            self.timeline.blockSignals(False)
            self.frame_label.setText(f"{self.current_frame}/{self.total_frames}")

    def on_crop_changed(self, rect):
        """Convert display-coordinate crop rect to original video coordinates."""
        if rect is None or rect.isEmpty():
            self.crop = None
            self.crop_info_label.setText(
                "None — drag on the preview to set a crop region"
            )
            return

        # The pixmap is centered inside the label — subtract the centering offset
        x_offset = max(0, (self.video_label.width() - self._render_w) // 2)
        y_offset = max(0, (self.video_label.height() - self._render_h) // 2)
        scale = self.orig_width / self._render_w

        def to_even(n):
            return (int(n) >> 1) << 1

        x = to_even((rect.x() - x_offset) * scale)
        y = to_even((rect.y() - y_offset) * scale)
        w = to_even(rect.width() * scale)
        h = to_even(rect.height() * scale)

        # Clamp to video bounds
        x = max(0, min(x, self.orig_width - 2))
        y = max(0, min(y, self.orig_height - 2))
        w = min(w, self.orig_width - x)
        h = min(h, self.orig_height - y)

        if w >= 2 and h >= 2:
            self.crop = (x, y, w, h)
            self.crop_info_label.setText(f"{w}×{h} at ({x}, {y})")
        else:
            self.crop = None
            self.crop_info_label.setText(
                "None — drag on the preview to set a crop region"
            )

    def on_timeline_moved(self, position):
        """Update the frame counter immediately; debounce the actual seek."""
        self.is_playing = False
        self.play_btn.setText("Play")
        self.play_timer.stop()
        self._pending_frame = position
        self.frame_label.setText(f"{position}/{self.total_frames}")
        self._seek_timer.start(VIDEO_SEEK_DEBOUNCE_MS)

    def _seek_to_pending(self):
        """Perform the deferred frame seek after the slider settles."""
        self.current_frame = self._pending_frame
        self.update_frame()

    def toggle_play(self):
        """Toggle between play and pause."""
        if self.is_playing:
            self.is_playing = False
            self.play_btn.setText("Play")
            self.play_timer.stop()
        else:
            self.is_playing = True
            self.play_btn.setText("Pause")
            # Cap preview fps; advance multiple source frames per tick to compensate
            preview_fps = min(self.fps, VIDEO_PREVIEW_MAX_FPS)
            self._frames_per_tick = max(1, round(self.fps / preview_fps))
            self.play_timer.start(int(1000 / preview_fps))

    def play_video(self):
        """Advance by _frames_per_tick source frames during playback."""
        if self.is_playing and self.current_frame < self.end_frame:
            self.current_frame = min(
                self.current_frame + self._frames_per_tick, self.end_frame
            )
            self.update_frame()
        else:
            self.play_timer.stop()
            self.is_playing = False
            self.play_btn.setText("Play")

    def on_trim_changed(self):
        """Handle trim spinbox changes."""
        self.start_frame = self.trim_start.value()
        self.end_frame = self.trim_end.value()

    def prev_frame(self):
        """Step back one frame and pause."""
        self.play_timer.stop()
        self.is_playing = False
        self.play_btn.setText("Play")
        if self.current_frame > 0:
            self.current_frame -= 1
            self.update_frame()

    def next_frame(self):
        """Step forward one frame and pause."""
        self.play_timer.stop()
        self.is_playing = False
        self.play_btn.setText("Play")
        if self.current_frame < self.total_frames - 1:
            self.current_frame += 1
            self.update_frame()

    def set_start_frame(self):
        """Set trim start to the current frame."""
        self.trim_start.setValue(self.current_frame)

    def set_end_frame(self):
        """Set trim end to the current frame."""
        self.trim_end.setValue(self.current_frame)

    def apply_and_close(self):
        """Validate trim values and close dialog if valid."""
        self.start_frame = self.trim_start.value()
        self.end_frame = self.trim_end.value()

        if self.start_frame > self.end_frame:
            self.start_frame, self.end_frame = self.end_frame, self.start_frame
            self.trim_start.setValue(self.start_frame)
            self.trim_end.setValue(self.end_frame)

        self.accept()

    def on_rotation_changed(self, index):
        """Handle rotation changes."""
        self.rotation = index * 90
        self.update_frame()

    def _restore_values(self, values: dict):
        """Restore trim, rotation, and crop from a previous session."""
        fps = self.fps or 1
        start_time = values.get("start_time")
        duration = values.get("duration")
        if start_time is not None and duration is not None:
            start = max(0, min(int(start_time * fps), self.total_frames - 1))
            end = max(0, min(int((start_time + duration) * fps), self.total_frames - 1))
            self.trim_start.setValue(start)
            self.trim_end.setValue(end)
            self.start_frame = start
            self.end_frame = end
            self.current_frame = start

        rotation = values.get("rotation", 0)
        rotation_index = {0: 0, 90: 1, 180: 2, 270: 3}.get(rotation, 0)
        self.rotation_combo.setCurrentIndex(rotation_index)
        self.rotation = rotation

        self.crop = values.get("crop")
        if self.crop:
            x, y, w, h = self.crop
            self.crop_info_label.setText(f"{w}×{h} at ({x}, {y})")

    def keyPressEvent(self, event):
        """Keyboard shortcuts: Space=play/pause, Left=prev frame, Right=next frame."""
        key = event.key()
        if key == Qt.Key_Space:
            self.toggle_play()
        elif key == Qt.Key_Left:
            self.prev_frame()
        elif key == Qt.Key_Right:
            self.next_frame()
        else:
            super().keyPressEvent(event)

    def get_edit_values(self) -> dict:
        """Return the edited values."""
        return {
            "start_time": self.start_frame / self.fps,
            "duration": (self.end_frame - self.start_frame) / self.fps,
            "rotation": self.rotation,
            "crop": self.crop,
        }

    def closeEvent(self, event):
        """Clean up timer on close."""
        self.play_timer.stop()
        event.accept()
