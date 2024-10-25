from __future__ import annotations
import PySide6.QtCore
import PySide6.QtWidgets
from .. import pipeline


class pipeline_list_widget(PySide6.QtWidgets.QListWidget):
    __pipeline: pipeline.manager
    __selection_updating: bool
    __selection: list[int]

    selection_changed = PySide6.QtCore.Signal()

    @property
    def source_pipeline(self: pipeline_list_widget) -> pipeline.pipeline:
        return self.__pipeline.pipeline[min(self.__selection)]

    @property
    def target_pineline(self: pipeline_list_widget) -> pipeline.pipeline:
        return self.__pipeline.pipeline[max(self.__selection)]

    def __init__(
        self: pipeline_list_widget,
        pipeline: pipeline.manager,
        parent: PySide6.QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.__pipeline = pipeline
        self.__selection_updating = False
        self.addItems([p.name for p in pipeline.pipeline])
        self.__selection = [0, self.count() - 1]
        self.setSelectionMode(
            PySide6.QtWidgets.QListWidget.SelectionMode.MultiSelection
        )
        for i in self.__selection:
            self.__select(i, PySide6.QtCore.QItemSelectionModel.SelectionFlag.Select)
        self.itemSelectionChanged.connect(self.__selection_changed)

    def __select(
        self: pipeline_list_widget,
        index: int,
        command: PySide6.QtCore.QItemSelectionModel.SelectionFlag,
    ) -> None:
        self.selectionModel().select(self.model().createIndex(index, 0), command)

    @PySide6.QtCore.Slot()
    def __selection_changed(self: pipeline_list_widget) -> None:
        if self.__selection_updating:
            return
        self.__selection_updating = True
        try:
            for i in self.selectedIndexes():
                if i.row() not in self.__selection[1:]:
                    self.__selection.pop(0)
                    self.__selection.append(i.row())
            self.__select(0, PySide6.QtCore.QItemSelectionModel.SelectionFlag.Clear)
            for i in self.__selection:
                self.__select(
                    i, PySide6.QtCore.QItemSelectionModel.SelectionFlag.Select
                )
        finally:
            self.__selection_updating = False
        self.selection_changed.emit()

    def update_names(self: pipeline_list_widget) -> None:
        for item, pipe in enumerate(self.__pipeline.pipeline):
            self.item(item).setText(pipe.name)
