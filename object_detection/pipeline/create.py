import typing
from .. import config
from .grayscale import grayscale
from .pipeline import pipeline
from .screen_capture import screen_capture


def create(config: config.config) -> typing.Generator[pipeline, None, None]:
    yield screen_capture(config.screen_capture)
    yield grayscale()
