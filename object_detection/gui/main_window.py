from __future__ import annotations
import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtMultimediaWidgets
import PySide6.QtWidgets
from .. import pipeline
from .pipeline_list_widget import pipeline_list_widget


class main_window(PySide6.QtWidgets.QMainWindow):
    def __init__(self: main_window, pipeline: list[pipeline.pipeline]) -> None:
        super().__init__()

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")

        new_action = PySide6.QtGui.QAction(
            PySide6.QtGui.QIcon.fromTheme("DocumentNew"),
            "&New",
            self,
        )
        new_action.setShortcuts(PySide6.QtGui.QKeySequence.StandardKey.New)
        new_action.setStatusTip("Discard the current video buffer")
        new_action.triggered.connect(self.clear_video_buffer)
        file_menu.addAction(new_action)  # pyright: ignore[reportUnknownMemberType]

        open_action = PySide6.QtGui.QAction(
            PySide6.QtGui.QIcon.fromTheme("DocumentOpen"),
            "&Open",
            self,
        )
        open_action.setShortcuts(PySide6.QtGui.QKeySequence.StandardKey.Open)
        open_action.setStatusTip("Play back a recorded video file")
        open_action.triggered.connect(self.open_video_for_playback)
        file_menu.addAction(open_action)  # pyright: ignore[reportUnknownMemberType]

        save_action = PySide6.QtGui.QAction(
            PySide6.QtGui.QIcon.fromTheme("DocumentSave"),
            "&Save",
            self,
        )
        save_action.setShortcuts(PySide6.QtGui.QKeySequence.StandardKey.Save)
        save_action.setStatusTip("Save the current video buffer")
        save_action.triggered.connect(self.save_video_buffer)
        file_menu.addAction(save_action)  # pyright: ignore[reportUnknownMemberType]

        save_as_action = PySide6.QtGui.QAction(
            PySide6.QtGui.QIcon.fromTheme("DocumentSaveAs"),
            "&Save As",
            self,
        )
        save_as_action.setShortcuts(PySide6.QtGui.QKeySequence.StandardKey.SaveAs)
        save_as_action.setStatusTip("Save the current video buffer")
        save_as_action.triggered.connect(self.save_video_buffer_as)
        file_menu.addAction(save_as_action)  # pyright: ignore[reportUnknownMemberType]

        central_widget = PySide6.QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        layout = PySide6.QtWidgets.QGridLayout(central_widget)
        central_widget.setLayout(layout)

        pipeline_list = pipeline_list_widget(pipeline, central_widget)
        layout.addWidget(pipeline_list, 0, 0, 1, 1)

        config_widget = PySide6.QtWidgets.QWidget(central_widget)
        layout.addWidget(config_widget, 1, 0, 2, 1)

        config_layout = PySide6.QtWidgets.QFormLayout(config_widget)
        config_widget.setLayout(config_layout)

        input_video = PySide6.QtMultimediaWidgets.QVideoWidget(central_widget)
        layout.addWidget(input_video, 0, 1, 2, 1)

        output_video = PySide6.QtMultimediaWidgets.QVideoWidget(central_widget)
        layout.addWidget(output_video, 0, 2, 2, 1)

        media_controls_widget = PySide6.QtWidgets.QWidget(central_widget)
        layout.addWidget(media_controls_widget, 1, 2, 2, 1)

        media_controls_layout = PySide6.QtWidgets.QHBoxLayout(media_controls_widget)
        media_controls_widget.setLayout(media_controls_layout)

    @PySide6.QtCore.Slot()
    def clear_video_buffer(self: main_window) -> None:
        pass

    @PySide6.QtCore.Slot()
    def open_video_for_playback(self: main_window) -> None:
        pass

    @PySide6.QtCore.Slot()
    def save_video_buffer(self: main_window) -> None:
        pass

    @PySide6.QtCore.Slot()
    def save_video_buffer_as(self: main_window) -> None:
        pass
