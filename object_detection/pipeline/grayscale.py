from __future__ import annotations
import cv2
from .pipeline import pipeline


class grayscale(pipeline):
    @pipeline.name.getter
    def name(self: grayscale) -> str:
        return "Color to Grayscale"

    def process(self: grayscale, source: cv2.typing.MatLike) -> cv2.typing.MatLike:
        return cv2.cvtColor(source, cv2.COLOR_RGB2GRAY)
