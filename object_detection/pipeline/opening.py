from __future__ import annotations
import cv2
from .. import config
from .pipeline import pipeline


class opening(pipeline):
    __config: config.sections.morphology

    @pipeline.name.getter
    def name(self: opening) -> str:
        return "Erosion & Dilation"

    def __init__(self: opening, config: config.sections.morphology) -> None:
        super().__init__()
        self.__config = config

    def process(self: opening, source: cv2.typing.MatLike) -> cv2.typing.MatLike:
        return cv2.morphologyEx(
            source,
            cv2.MORPH_OPEN,
            cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE,
                (self.__config.opening_width, self.__config.opening_height),
            ),
        )
