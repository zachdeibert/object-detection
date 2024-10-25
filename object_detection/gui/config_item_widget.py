from __future__ import annotations
import PySide6.QtCore
import PySide6.QtWidgets
import typing
from .. import config

if typing.TYPE_CHECKING:
    from .config_widget import config_widget

T = typing.TypeVar("T", bound=config.base)


class config_item_widget(PySide6.QtWidgets.QLineEdit):
    __normalizer: typing.Callable[[str], str]
    __setter: typing.Callable[[str], None]
    __valid_text: str
    __validators: list[typing.Callable[[str], bool]]

    def __init__(self: config_item_widget, parent: config_widget, label: str) -> None:
        super().__init__(parent)
        self.__validators = []
        self.textEdited.connect(self.text_edited)
        parent.form_layout.addRow(label, self)

    @PySide6.QtCore.Slot()
    def text_edited(self: config_item_widget) -> None:
        raw_text = self.text()
        try:
            text = self.__normalizer(raw_text)
        except ValueError:
            self.setText(self.__valid_text)
            return
        for validator in self.__validators:
            if not validator(text):
                self.setText(self.__valid_text)
                return
        self.__valid_text = text
        if text != raw_text:
            self.setText(text)
        self.__setter(text)

    def floating(
        self: config_item_widget,
        base: T,
        getter: typing.Callable[[T], float],
        name: str,
    ) -> config_item_widget:
        self.__normalizer = lambda t: str(float(t)) if len(t) > 0 else "0"
        self.__setter = lambda t: setattr(base, name, float(t))
        self.__valid_text = str(getter(base))
        self.setText(self.__valid_text)
        return self

    def integer(
        self: config_item_widget, base: T, getter: typing.Callable[[T], int], name: str
    ) -> config_item_widget:
        self.__normalizer = lambda t: str(int(t)) if len(t) > 0 else "0"
        self.__setter = lambda t: setattr(base, name, int(t))
        self.__valid_text = str(getter(base))
        self.setText(self.__valid_text)
        return self

    def nonnegative(self: config_item_widget) -> config_item_widget:
        self.__validators.append(lambda t: not t.startswith("-"))
        return self

    def range(
        self: config_item_widget, min_inclusive: float, max_exclusive: float
    ) -> config_item_widget:
        self.__validators.append(lambda t: min_inclusive <= float(t) < max_exclusive)
        return self
