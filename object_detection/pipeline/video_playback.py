from __future__ import annotations
import cv2
import threading
from .source import source


class video_playback(source):
    __lock: threading.Lock
    __video: cv2.VideoCapture

    @source.frame.setter
    def frame(self: video_playback, frame: int) -> None:
        with self.__lock:
            self.__video.set(cv2.CAP_PROP_POS_FRAMES, frame)

    @source.name.getter
    def name(self: video_playback) -> str:
        return "Video Playback"

    def __init__(self: video_playback, filename: str) -> None:
        self.__lock = threading.Lock()
        self.__video = cv2.VideoCapture(filename)
        super().__init__(
            self.__video.get(cv2.CAP_PROP_FPS),
            int(self.__video.get(cv2.CAP_PROP_FRAME_COUNT)),
        )

    def capture(self: video_playback) -> cv2.typing.MatLike | None:
        with self.__lock:
            success, frame = self.__video.read()
        if success:
            return frame
        else:
            return None
