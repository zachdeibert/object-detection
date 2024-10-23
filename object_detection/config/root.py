from __future__ import annotations
import contextlib
import json
import os
import threading
import time
import types
import typing
from .base import base

_dtype: typing.TypeAlias = "dict[str, str | _dtype]"


class root(base, contextlib.AbstractContextManager[None]):
    __autosave: float | None
    __cond: threading.Condition
    __data: _dtype
    __filename: str
    __shutdown: bool
    __thread: threading.Thread

    def __init__(self: root, filename: str) -> None:
        self.__filename = os.path.abspath(filename)
        try:
            with open(self.__filename, "r") as f:
                self.__data = json.load(f)
        except FileNotFoundError:
            self.__data = {}
        super().__init__(self.__data, self.__update)

    def __enter__(self: root) -> None:
        self.__autosave = None
        self.__cond = threading.Condition(threading.Lock())
        self.__shutdown = False
        self.__thread = threading.Thread(
            target=self.__thread_func, name="Config Auto-Save"
        )
        self.__thread.start()

    def __exit__(
        self: root,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        with self.__cond:
            self.__shutdown = True
            self.__cond.notify()
        self.__thread.join()

    def __thread_func(self: root) -> None:
        while True:
            with self.__cond:
                if self.__shutdown:
                    break
                if self.__autosave is None:
                    self.__cond.wait()
                    continue
                timeout = self.__autosave - time.time()
                if timeout > 0 and self.__cond.wait(timeout):
                    continue
                self.__autosave = None
            self.__save()
        if self.__autosave is not None:
            self.__save()

    def __save(self: root) -> None:
        with open(self.__filename + "~", "w") as f:
            json.dump(self.__data, f, indent=4)
            f.write("\n")
        os.replace(self.__filename + "~", self.__filename)

    def __update(self: root) -> None:
        try:
            cond = self.__cond
        except AttributeError:
            self.__save()
        else:
            with cond:
                self.__autosave = time.time() + 10
                cond.notify()
