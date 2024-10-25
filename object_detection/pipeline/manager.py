from __future__ import annotations
import contextlib
import types
from .. import config
from .grayscale import grayscale
from .pipeline import pipeline
from .screen_capture import screen_capture
from .source import source
from .video_playback import video_playback


class manager(contextlib.AbstractContextManager["manager"]):
    __config: config.config
    __pipeline: list[pipeline]
    __source: source

    @property
    def pipeline(self: manager) -> list[pipeline]:
        return self.__pipeline

    @property
    def source(self: manager) -> source:
        return self.__source

    def __init__(self: manager, config: config.config) -> None:
        super().__init__()
        self.__config = config
        self.__source = screen_capture(config.screen_capture)
        self.__pipeline = [
            self.__source,
            grayscale(),
        ]
        for source, sink in zip(self.__pipeline, self.__pipeline[1:]):
            source.chain(sink)

    def __enter__(self: manager) -> manager:
        return self

    def __exit__(
        self: manager,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        self.close()

    def close(self: manager) -> None:
        self.__source.close()

    def open_capture(self: manager) -> None:
        self.__source.close()
        self.__source = screen_capture(self.__config.screen_capture)
        self.__pipeline[0] = self.__source
        self.__source.chain(self.__pipeline[1])

    def open_playback(self: manager, filename: str) -> None:
        self.__source.close()
        self.__source = video_playback(filename)
        self.__pipeline[0] = self.__source
        self.__source.chain(self.__pipeline[1])
