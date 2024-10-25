from __future__ import annotations
import araviq6
import cv2
import PySide6.QtMultimediaWidgets
import PySide6.QtWidgets
from .. import pipeline


class video_widget(PySide6.QtMultimediaWidgets.QVideoWidget):
    __source: pipeline.pipeline | None
    __subscription: pipeline.subscription

    @property
    def source(self: video_widget) -> pipeline.pipeline | None:
        return self.__source

    @source.setter
    def source(self: video_widget, source: pipeline.pipeline | None) -> None:
        if self.__source != source:
            if self.__source is not None:
                self.__subscription.close()
            self.__source = source
            if source is not None:
                self.__subscription = pipeline.subscription()
                source.subscribe(self.__update, self.__subscription)

    def __init__(
        self: video_widget, parent: PySide6.QtWidgets.QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.__source = None

    def __update(self: video_widget, frame: cv2.typing.MatLike) -> None:
        self.videoSink().setVideoFrame(
            araviq6.array2qvideoframe(frame)  # pyright: ignore[reportUnknownMemberType]
        )
