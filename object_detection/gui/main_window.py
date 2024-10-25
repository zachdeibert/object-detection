from __future__ import annotations
import os
import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtWidgets
from .. import config, pipeline
from .config_widget import config_widget
from .pipeline_list_widget import pipeline_list_widget
from .video_widget import video_widget


class main_window(PySide6.QtWidgets.QMainWindow):
    __input_video: video_widget
    __output_video: video_widget
    __pipeline_manager: pipeline.manager
    __pipeline: pipeline_list_widget

    def __init__(
        self: main_window, config: config.config, pipeline: pipeline.manager
    ) -> None:
        super().__init__()
        self.__pipeline_manager = pipeline

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
        save_action.setStatusTip("Record a video file")
        save_action.triggered.connect(self.save_video_buffer)
        file_menu.addAction(save_action)  # pyright: ignore[reportUnknownMemberType]

        central_widget = PySide6.QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        layout = PySide6.QtWidgets.QGridLayout(central_widget)
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 0)
        central_widget.setLayout(layout)

        self.__pipeline = pipeline_list_widget(pipeline, central_widget)
        self.__pipeline.selection_changed.connect(self.pipeline_selection_changed)
        layout.addWidget(self.__pipeline, 0, 0, 1, 1)

        config_ui_container = PySide6.QtWidgets.QScrollArea(self)
        config_ui_container.setHorizontalScrollBarPolicy(
            PySide6.QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        config_ui_container.setVerticalScrollBarPolicy(
            PySide6.QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        layout.addWidget(config_ui_container, 1, 0, 2, 1)

        config_ui = config_widget(config, config_ui_container)
        config_ui_container.setWidget(config_ui)
        config_ui_container.setWidgetResizable(True)

        self.__input_video = video_widget(central_widget)
        layout.addWidget(self.__input_video, 0, 1, 2, 1)

        self.__output_video = video_widget(central_widget)
        layout.addWidget(self.__output_video, 0, 2, 2, 1)

        media_controls_widget = PySide6.QtWidgets.QWidget(central_widget)
        layout.addWidget(media_controls_widget, 1, 2, 2, 1)

        media_controls_layout = PySide6.QtWidgets.QHBoxLayout(media_controls_widget)
        media_controls_widget.setLayout(media_controls_layout)

        self.pipeline_selection_changed()

    @PySide6.QtCore.Slot()
    def clear_video_buffer(self: main_window) -> None:
        self.__pipeline_manager.open_capture()
        self.__pipeline.update_names()
        self.pipeline_selection_changed()

    @PySide6.QtCore.Slot()
    def open_video_for_playback(self: main_window) -> None:
        dialog = PySide6.QtWidgets.QFileDialog(
            self,
            "Open Video",
            os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir)),
            "Video Files (*.mp4)",
        )
        dialog.setAcceptMode(PySide6.QtWidgets.QFileDialog.AcceptMode.AcceptOpen)
        dialog.setFileMode(PySide6.QtWidgets.QFileDialog.FileMode.ExistingFile)
        dialog.setViewMode(PySide6.QtWidgets.QFileDialog.ViewMode.Detail)
        if dialog.exec():
            self.__pipeline_manager.open_playback(dialog.selectedFiles()[0])
            self.__pipeline.update_names()
            self.pipeline_selection_changed()

    @PySide6.QtCore.Slot()
    def pipeline_selection_changed(self: main_window) -> None:
        self.__input_video.source = self.__pipeline.source_pipeline
        self.__output_video.source = self.__pipeline.target_pineline

    @PySide6.QtCore.Slot()
    def save_video_buffer(self: main_window) -> None:
        dialog = PySide6.QtWidgets.QFileDialog(
            self,
            "Save Video",
            os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir)),
            "Video Files (*.mp4)",
        )
        dialog.setAcceptMode(PySide6.QtWidgets.QFileDialog.AcceptMode.AcceptSave)
        dialog.setFileMode(PySide6.QtWidgets.QFileDialog.FileMode.AnyFile)
        dialog.setViewMode(PySide6.QtWidgets.QFileDialog.ViewMode.Detail)
        if dialog.exec():
            self.__pipeline_manager.record(dialog.selectedFiles()[0])
