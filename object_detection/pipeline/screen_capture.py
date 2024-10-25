from __future__ import annotations
import cv2
import mss
import mss.base
import numpy
from .. import config
from .source import source


class screen_capture(source):
    __config: config.sections.screen_capture
    __mss: mss.base.MSSBase

    @source.name.getter
    def name(self: screen_capture) -> str:
        return "Screen Capture"

    def __init__(self: screen_capture, config: config.sections.screen_capture) -> None:
        self.__config = config
        super().__init__(30.0)

    def _thread_init(self: screen_capture) -> None:
        self.__mss = mss.mss()

    def _thread_deinit(self: screen_capture) -> None:
        self.__mss.close()

    def capture(self: screen_capture) -> cv2.typing.MatLike:
        monitors = self.__mss.monitors
        monitor_idx = self.__config.monitor
        if monitor_idx + 1 >= len(monitors):
            monitor = monitors[0]
        else:
            monitor = monitors[monitor_idx + 1]
        return cv2.cvtColor(
            numpy.array(
                self.__mss.grab(
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
                            monitor["width"] - self.__config.left - self.__config.right,
                        ),
                    }
                )
            ),
            cv2.COLOR_BGRA2RGB,
        )
