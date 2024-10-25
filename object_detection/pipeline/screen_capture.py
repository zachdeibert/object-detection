from __future__ import annotations
import cv2
import mss
import numpy
import threading
import time
from .. import config
from .pipeline import pipeline


class screen_capture(pipeline):
    __close: threading.Event
    __config: config.sections.screen_capture
    __thread: threading.Thread

    @pipeline.name.getter
    def name(self: screen_capture) -> str:
        return "Screen Capture"

    def __init__(self: screen_capture, config: config.sections.screen_capture) -> None:
        super().__init__()
        self.__close = threading.Event()
        self.__config = config
        self.__thread = threading.Thread(
            target=self.__thread_func, name="Screen Capture"
        )
        self.__thread.start()

    def __thread_func(self: screen_capture) -> None:
        with mss.mss() as sct:
            while True:
                start = time.time()
                monitors = sct.monitors
                monitor_idx = self.__config.monitor
                if monitor_idx + 1 >= len(monitors):
                    monitor = monitors[0]
                else:
                    monitor = monitors[monitor_idx + 1]
                self.publish(
                    cv2.cvtColor(
                        numpy.array(
                            sct.grab(
                                {
                                    "height": max(
                                        1,
                                        monitor["height"]
                                        - self.__config.top
                                        - self.__config.bottom,
                                    ),
                                    "left": monitor["left"] + self.__config.left,
                                    "top": monitor["top"] + self.__config.top,
                                    "width": max(
                                        1,
                                        monitor["width"]
                                        - self.__config.left
                                        - self.__config.right,
                                    ),
                                }
                            )
                        ),
                        cv2.COLOR_BGRA2RGB,
                    )
                )
                if self.__close.wait(max(0, 1 / 30 - (time.time() - start))):
                    break

    def close(self: screen_capture) -> None:
        self.__close.set()
        self.__thread.join()

    def process(self: screen_capture, source: cv2.typing.MatLike) -> cv2.typing.MatLike:
        raise RuntimeError("screen_capture should never sink any frames")
