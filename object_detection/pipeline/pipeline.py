from __future__ import annotations
import abc


class pipeline(abc.ABC):
    @property
    def name(self: pipeline) -> str:
        raise NotImplementedError("object_detection.pipeline.pipeline.name")
