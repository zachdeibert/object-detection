from __future__ import annotations
import abc
import cv2
import threading
import time
from .pipeline import pipeline


class source(pipeline):
    __closed: bool
    __cond: threading.Condition
    __default_framerate: float
    __frame: int
    __framerate: float
    __length: int
    __thread: threading.Thread

    @property
    def default_framerate(self: source) -> float:
        return self.__default_framerate

    @property
    def frame(self: source) -> int:
        return self.__frame

    @frame.setter
    def frame(self, frame: int) -> None:
        pass

    @property
    def framerate(self: source) -> float:
        return self.__framerate

    @framerate.setter
    def framerate(self: source, framerate: float) -> None:
        with self.__cond:
            if framerate == 0:
                self.__framerate = 1 / (86400 * 365)
            else:
                self.__framerate = framerate
            self.__cond.notify()

    @property
    def length(self: source) -> int:
        return max(self.__frame, self.__length)

    def __init__(self: source, framerate: float, length: int = 0) -> None:
        super().__init__()
        self.__closed = False
        self.__cond = threading.Condition()
        self.__default_framerate = framerate
        self.__frame = 0
        self.__framerate = framerate
        self.__length = length
        self.__thread = threading.Thread(
            target=self.__thread_func, name=self.__class__.__name__
        )
        self.__thread.start()

    def __thread_func(self: source) -> None:
        self._thread_init()
        try:
            last = time.time()
            while True:
                with self.__cond:
                    while True:
                        if self.__closed:
                            return
                        next = last + 1 / self.__framerate
                        timeout = next - time.time()
                        if timeout <= 0:
                            break
                        self.__cond.wait(timeout)
                frame = self.capture()
                if frame is not None:
                    self.publish(frame)
                    self.__frame += 1
                last = next
                now = time.time()
                if now > last + 1 / self.__framerate:
                    last = now
        finally:
            self._thread_deinit()

    def _thread_deinit(self: source) -> None:
        pass

    def _thread_init(self: source) -> None:
        pass

    @abc.abstractmethod
    def capture(self: source) -> cv2.typing.MatLike | None:
        raise NotImplementedError("object_detection.pipeline.source.capture")

    def close(self: source) -> None:
        with self.__cond:
            self.__closed = True
            self.__cond.notify()
        self.__thread.join()

    def process(self: source, source: cv2.typing.MatLike) -> cv2.typing.MatLike:
        raise RuntimeError("source should never sink any frames")
