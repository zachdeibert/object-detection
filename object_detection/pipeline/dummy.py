from __future__ import annotations
from .pipeline import pipeline


class dummy(pipeline):
    __name: str

    @pipeline.name.getter
    def name(self: dummy) -> str:
        return self.__name

    def __init__(self: dummy, name: str) -> None:
        super().__init__()
        self.__name = name
