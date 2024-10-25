from __future__ import annotations
import cv2
import skvideo.io  # pyright: ignore[reportMissingTypeStubs]
import threading
from .pipeline import pipeline
from .source import source
from .subscription import subscription


class video_recording(pipeline):
    __closed: bool
    __lock: threading.Lock
    __token: subscription
    __video: skvideo.io.FFmpegWriter

    @pipeline.name.getter
    def name(self: video_recording) -> str:
        return "Video Recording"

    def __init__(self: video_recording, filename: str, source: source) -> None:
        super().__init__()
        self.__closed = False
        self.__lock = threading.Lock()
        self.__token = subscription()
        self.__video = skvideo.io.FFmpegWriter(
            filename,
            outputdict={
                "-filter:v": f"fps={source.default_framerate}",
                "-vcodec": "libx264",
            },
        )
        source.chain(self, self.__token)

    def close(self: video_recording) -> None:
        with self.__lock:
            self.__closed = True
        self.__token.close()
        self.__video.close()

    def process(
        self: video_recording, source: cv2.typing.MatLike
    ) -> cv2.typing.MatLike:
        with self.__lock:
            if not self.__closed:
                self.__video.writeFrame(  # pyright: ignore[reportUnknownMemberType]
                    source
                )
        return source
