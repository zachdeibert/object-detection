from __future__ import annotations
import cv2
from .. import config
from .pipeline import pipeline


class bbox(pipeline):
    __config: config.sections.threshold
    __source: cv2.typing.MatLike

    @pipeline.name.getter
    def name(self: bbox) -> str:
        return "Bounding Boxes"

    def __init__(self: bbox, config: config.sections.threshold) -> None:
        super().__init__()
        self.__config = config

    def process_original(self: bbox, source: cv2.typing.MatLike) -> None:
        self.__source = source

    def process(self: bbox, source: cv2.typing.MatLike) -> cv2.typing.MatLike:
        frame = self.__source.copy()
        contour_size = self.__config.contour_size
        contour_per_y = self.__config.contour_per_y
        height = source.shape[1]
        for contour in cv2.findContours(
            source, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )[0]:
            x, y, w, h = cv2.boundingRect(contour)
            if cv2.contourArea(contour) > contour_size - contour_per_y * (
                height - (y + h / 2)
            ):
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 3)
        return frame
