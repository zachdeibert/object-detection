from __future__ import annotations
import PySide6.QtCore
import PySide6.QtWidgets
from .. import pipeline


class video_controls_widget(PySide6.QtWidgets.QWidget):
    __label: PySide6.QtWidgets.QLabel
    __play_pause: PySide6.QtWidgets.QToolButton
    __pipeline: pipeline.manager
    __slider: PySide6.QtWidgets.QSlider
    __timer: PySide6.QtCore.QTimer

    def __init__(
        self: video_controls_widget,
        pipeline: pipeline.manager,
        parent: PySide6.QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.__pipeline = pipeline

        layout = PySide6.QtWidgets.QHBoxLayout(self)
        self.setLayout(layout)

        self.__slider = PySide6.QtWidgets.QSlider(
            PySide6.QtCore.Qt.Orientation.Horizontal, self
        )
        self.__slider.sliderMoved.connect(self.slider_moved)
        layout.addWidget(self.__slider)

        self.__label = PySide6.QtWidgets.QLabel("00:00:00 / 00:00:00", self)
        layout.addWidget(self.__label)

        fast_reverse = PySide6.QtWidgets.QToolButton(self)
        fast_reverse.setIcon(
            self.style().standardIcon(
                PySide6.QtWidgets.QStyle.StandardPixmap.SP_MediaSeekBackward
            )
        )
        fast_reverse.clicked.connect(self.fast_reverse)
        layout.addWidget(fast_reverse)

        self.__play_pause = PySide6.QtWidgets.QToolButton(self)
        self.__play_pause.setIcon(
            self.style().standardIcon(
                PySide6.QtWidgets.QStyle.StandardPixmap.SP_MediaPause
            )
        )
        self.__play_pause.clicked.connect(self.play_pause)
        layout.addWidget(self.__play_pause)

        fast_forward = PySide6.QtWidgets.QToolButton(self)
        fast_forward.setIcon(
            self.style().standardIcon(
                PySide6.QtWidgets.QStyle.StandardPixmap.SP_MediaSeekForward
            )
        )
        fast_forward.clicked.connect(self.fast_forward)
        layout.addWidget(fast_forward)

        self.__timer = PySide6.QtCore.QTimer(self)
        self.__timer.setSingleShot(False)
        self.__timer.timeout.connect(self.update_time)
        self.__timer.start(250)

    @PySide6.QtCore.Slot()
    def fast_forward(self: video_controls_widget) -> None:
        if self.__pipeline.source.framerate < self.__pipeline.source.default_framerate:
            self.__pipeline.source.framerate = self.__pipeline.source.default_framerate
        else:
            self.__pipeline.source.framerate += self.__pipeline.source.default_framerate

    @PySide6.QtCore.Slot()
    def fast_reverse(self: video_controls_widget) -> None:
        if (
            self.__pipeline.source.framerate == 0
            or self.__pipeline.source.framerate
            > self.__pipeline.source.default_framerate
        ):
            self.__pipeline.source.framerate = self.__pipeline.source.default_framerate
        else:
            self.__pipeline.source.framerate = (
                self.__pipeline.source.default_framerate
                / (
                    self.__pipeline.source.default_framerate
                    / self.__pipeline.source.framerate
                    + 1
                )
            )

    @PySide6.QtCore.Slot()
    def play_pause(self: video_controls_widget) -> None:
        if self.__pipeline.source.framerate:
            self.__pipeline.source.framerate = 0
            self.__play_pause.setIcon(
                self.style().standardIcon(
                    PySide6.QtWidgets.QStyle.StandardPixmap.SP_MediaPlay
                )
            )
        else:
            self.play()

    def play(self: video_controls_widget) -> None:
        self.__pipeline.source.framerate = self.__pipeline.source.default_framerate
        self.__play_pause.setIcon(
            self.style().standardIcon(
                PySide6.QtWidgets.QStyle.StandardPixmap.SP_MediaPause
            )
        )

    @PySide6.QtCore.Slot()
    def slider_moved(self: video_controls_widget) -> None:
        self.__pipeline.source.frame = self.__slider.sliderPosition()

    @PySide6.QtCore.Slot()
    def update_time(self: video_controls_widget) -> None:
        framerate = self.__pipeline.source.default_framerate
        position = self.__pipeline.source.frame
        length = self.__pipeline.source.length
        self.__slider.setMaximum(length)
        self.__slider.setSliderPosition(position)
        self.__label.setText(
            f"{self.__format_time(position / framerate)} / {self.__format_time(length / framerate)}"
        )

    def __format_time(self: video_controls_widget, secs: float) -> str:
        secs = int(secs)
        mins = secs // 60
        secs %= 60
        hours = mins // 60
        mins %= 60
        return f"{hours:02d}:{mins:02d}:{secs:02d}"
