from __future__ import annotations
import threading
import typing


class subscription:
    __lock: threading.Lock
    __on_unsubscribe: list[typing.Callable[[], None]]
    __subscribed: bool

    def __init__(self: subscription) -> None:
        self.__lock = threading.Lock()
        self.__on_unsubscribe = []
        self.__subscribed = True

    def close(self: subscription) -> None:
        with self.__lock:
            if not self.__subscribed:
                return
            self.__subscribed = False
        for callback in self.__on_unsubscribe:
            callback()
        del self.__on_unsubscribe

    def on_unsubscribe(self: subscription, callback: typing.Callable[[], None]) -> None:
        with self.__lock:
            if self.__subscribed:
                self.__on_unsubscribe.append(callback)
                return
        callback()
