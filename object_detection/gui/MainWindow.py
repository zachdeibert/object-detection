from __future__ import annotations
import PySide6.QtCore
import PySide6.QtWidgets


class MainWindow(PySide6.QtWidgets.QWidget):
    def __init__(self: MainWindow) -> None:
        super().__init__()
        text = PySide6.QtWidgets.QLabel("Hello, world!")
        text.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
        layout = PySide6.QtWidgets.QVBoxLayout(self)
        layout.addWidget(text)
        self.setLayout(layout)
