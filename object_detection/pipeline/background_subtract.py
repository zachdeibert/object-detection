from __future__ import annotations
import cv2
from .pipeline import pipeline


class background_subtract(pipeline):
    __subtractor: cv2.BackgroundSubtractorMOG2

    @pipeline.name.getter
    def name(self: background_subtract) -> str:
        return "Background Subtraction"

    def __init__(self: background_subtract) -> None:
        super().__init__()
        self.__subtractor = cv2.createBackgroundSubtractorMOG2()

    def process(
        self: background_subtract, source: cv2.typing.MatLike
    ) -> cv2.typing.MatLike:
        return self.__subtractor.apply(source)
