from __future__ import annotations
import cv2
from .. import config
from .pipeline import pipeline


class threshold(pipeline):
    __config: config.sections.threshold

    @pipeline.name.getter
    def name(self: threshold) -> str:
        return "Thresholding"

    def __init__(self: threshold, config: config.sections.threshold) -> None:
        super().__init__()
        self.__config = config

    def process(self: threshold, source: cv2.typing.MatLike) -> cv2.typing.MatLike:
        return cv2.threshold(
            source, self.__config.value, self.__config.maximum, cv2.THRESH_BINARY
        )[1]
