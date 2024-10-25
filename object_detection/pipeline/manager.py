from __future__ import annotations
import contextlib
import types
from .. import config
from .background_subtract import background_subtract
from .bbox import bbox
from .opening import opening
from .pipeline import pipeline
from .screen_capture import screen_capture
from .source import source
from .threshold import threshold
from .video_playback import video_playback
from .video_recording import video_recording


class manager(contextlib.AbstractContextManager["manager"]):
    __bbox: bbox
    __config: config.config
    __pipeline: list[pipeline]
    __source: source
    __recording: video_recording | None

    @property
    def pipeline(self: manager) -> list[pipeline]:
        return self.__pipeline

    @property
    def source(self: manager) -> source:
        return self.__source

    def __init__(self: manager, config: config.config) -> None:
        super().__init__()
        self.__bbox = bbox(config.threshold)
        self.__config = config
        self.__source = screen_capture(config.screen_capture)
        self.__pipeline = [
            self.__source,
            background_subtract(),
            threshold(config.threshold),
            opening(),
            self.__bbox,
        ]
        self.__recording = None
        self.__source.subscribe(self.__bbox.process_original)
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
        if self.__recording is not None:
            self.__recording.close()
            self.__recording = None

    def open_capture(self: manager) -> None:
        self.__open(screen_capture(self.__config.screen_capture))

    def open_playback(self: manager, filename: str) -> None:
        self.__open(video_playback(filename))

    def __open(self: manager, source: source) -> None:
        self.close()
        self.__source = source
        self.__pipeline[0] = self.__source
        self.__source.subscribe(self.__bbox.process_original)
        self.__source.chain(self.__pipeline[1])

    def record(self: manager, filename: str) -> None:
        if self.__recording is not None:
            self.__recording.close()
        self.__recording = video_recording(filename, self.__source)
