from __future__ import annotations
import abc
import cv2
import threading
import traceback
import typing
from .subscription import subscription


class pipeline(abc.ABC):
    __lock: threading.Lock
    __next_id: int
    __subscriptions: dict[int, typing.Callable[[cv2.typing.MatLike], None]]

    @property
    @abc.abstractmethod
    def name(self: pipeline) -> str:
        raise NotImplementedError("object_detection.pipeline.pipeline.name")

    def __init__(self: pipeline) -> None:
        super().__init__()
        self.__lock = threading.Lock()
        self.__next_id = 0
        self.__subscriptions = {}

    def chain(
        self: pipeline, next: pipeline, token: subscription | None = None
    ) -> None:
        self.subscribe(lambda source: next.publish(next.process(source)), token)

    @abc.abstractmethod
    def process(self: pipeline, source: cv2.typing.MatLike) -> cv2.typing.MatLike:
        raise NotImplementedError("object_detection.pipeline.pipeline.process")

    def publish(self: pipeline, result: cv2.typing.MatLike) -> None:
        with self.__lock:
            subscriptions = list(self.__subscriptions.values())
        for subscription in subscriptions:
            try:
                subscription(result)
            except:
                traceback.print_exc()

    def subscribe(
        self: pipeline,
        callback: typing.Callable[[cv2.typing.MatLike], None],
        token: subscription | None = None,
    ) -> None:
        with self.__lock:
            id = self.__next_id
            self.__next_id += 1
            self.__subscriptions[id] = callback
        if token is not None:

            def unsubscribe() -> None:
                with self.__lock:
                    del self.__subscriptions[id]

            token.on_unsubscribe(unsubscribe)
