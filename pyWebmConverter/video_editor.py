"""
Video editor dialog for trimming, rotating, and scaling videos.
Provides preview and editing capabilities for WebM conversion.
"""

import cv2
from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QSlider,
    QSpinBox,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
from .constants import VIDEO_EDITOR_WIDTH, VIDEO_EDITOR_HEIGHT, VIDEO_PREVIEW_WIDTH


class VideoEditorDialog(QDialog):
    """
    A separate dialog for video preview and editing.
    Allows users to trim, rotate, and scale video clips.
    """

    def __init__(self, video_path, parent=None):
        """
        Initialize the video editor dialog.

        Args:
            video_path: Path to the video file
            parent: Parent widget
        """
        super().__init__(parent)
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.current_frame = 0
        self.is_playing = False

        # Edit settings
        self.start_frame = 0
        self.end_frame = self.total_frames - 1
        self.rotation = 0  # 0, 90, 180, 270

        # Timer for playback
        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.play_video)

        self.init_ui()
        self.update_frame()

    def init_ui(self):
        """Set up the editor UI."""
        self.setWindowTitle("Video Editor")
        self.setGeometry(100, 100, VIDEO_EDITOR_WIDTH, VIDEO_EDITOR_HEIGHT)
        layout = QVBoxLayout()

        # Video display
        self.video_label = QLabel()
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setStyleSheet("background-color: black;")
        layout.addWidget(self.video_label)

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
            # Apply rotation
            if self.rotation == 90:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            elif self.rotation == 180:
                frame = cv2.rotate(frame, cv2.ROTATE_180)
            elif self.rotation == 270:
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Convert BGR to RGB and display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qt_image = QImage(
                frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaledToWidth(VIDEO_PREVIEW_WIDTH)
            self.video_label.setPixmap(scaled_pixmap)

            self.timeline.blockSignals(True)
            self.timeline.setValue(self.current_frame)
            self.timeline.blockSignals(False)
            self.frame_label.setText(f"{self.current_frame}/{self.total_frames}")

    def on_timeline_moved(self, position):
        """Handle timeline slider movement."""
        self.is_playing = False
        self.play_btn.setText("Play")
        self.current_frame = position
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
            # Start timer with frame interval (in milliseconds)
            frame_interval = int(1000 / self.fps)
            self.play_timer.start(frame_interval)

    def play_video(self):
        """Play video frames."""
        if self.is_playing and self.current_frame < self.end_frame:
            self.current_frame += 1
            self.update_frame()
        else:
            self.play_timer.stop()
            self.is_playing = False
            self.play_btn.setText("Play")

    def on_trim_changed(self):
        """Handle trim value changes."""
        self.start_frame = self.trim_start.value()
        self.end_frame = self.trim_end.value()

    def apply_and_close(self):
        """Validate trim values and close dialog if valid."""
        self.start_frame = self.trim_start.value()
        self.end_frame = self.trim_end.value()

        # Validate that start frame is not higher than end frame
        if self.start_frame > self.end_frame:
            # Auto-correct by swapping them
            self.start_frame, self.end_frame = self.end_frame, self.start_frame
            self.trim_start.setValue(self.start_frame)
            self.trim_end.setValue(self.end_frame)

        self.accept()

    def on_rotation_changed(self, index):
        """Handle rotation changes."""
        self.rotation = index * 90
        self.update_frame()

    def get_edit_values(self) -> dict:
        """Return the edited values."""
        start_time = self.start_frame / self.fps
        duration = (self.end_frame - self.start_frame) / self.fps
        return {
            "start_time": start_time,
            "duration": duration,
            "rotation": self.rotation,
        }

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

    def closeEvent(self, event):
        """Clean up timer on close."""
        self.play_timer.stop()
        event.accept()
