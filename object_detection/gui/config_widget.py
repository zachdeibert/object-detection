from __future__ import annotations
import PySide6.QtWidgets
from .. import config
from .config_item_widget import config_item_widget


class config_widget(PySide6.QtWidgets.QWidget):
    __layout: PySide6.QtWidgets.QFormLayout

    @property
    def form_layout(self: config_widget) -> PySide6.QtWidgets.QFormLayout:
        return self.__layout

    def __init__(
        self: config_widget,
        config: config.config,
        parent: PySide6.QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.__layout = PySide6.QtWidgets.QFormLayout(self)
        self.setLayout(self.__layout)

        self.__layout.addRow(PySide6.QtWidgets.QLabel("Screen Capture", self))
        config_item_widget(self, "Top Offset").integer(
            config.screen_capture, lambda c: c.top, "top"
        ).nonnegative()
        config_item_widget(self, "Left Offset").integer(
            config.screen_capture, lambda c: c.left, "left"
        ).nonnegative()
        config_item_widget(self, "Bottom Offset").integer(
            config.screen_capture, lambda c: c.bottom, "bottom"
        ).nonnegative()
        config_item_widget(self, "Right Offset").integer(
            config.screen_capture, lambda c: c.right, "right"
        ).nonnegative()
