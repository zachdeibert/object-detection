import typing
from .dummy import dummy
from .pipeline import pipeline


def create() -> typing.Generator[pipeline, None, None]:
    yield dummy("Video Capture")
    yield dummy("Stage 1")
    yield dummy("Stage 2")
    yield dummy("Stage 3")
    yield dummy("Stage 4")
    yield dummy("Stage 5")
    yield dummy("Final Stage")
