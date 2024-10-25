from __future__ import annotations
import cv2
from .pipeline import pipeline


class opening(pipeline):
    __kernel: cv2.typing.MatLike

    @pipeline.name.getter
    def name(self: opening) -> str:
        return "Erosion & Dilation"

    def __init__(self: opening) -> None:
        super().__init__()
        self.__kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    def process(self: opening, source: cv2.typing.MatLike) -> cv2.typing.MatLike:
        return cv2.morphologyEx(source, cv2.MORPH_OPEN, self.__kernel)
