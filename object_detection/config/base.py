from __future__ import annotations
import typing

_dtype: typing.TypeAlias = "dict[str, str | _dtype]"


class base:
    __data: _dtype
    __on_update: typing.Callable[[], None]

    def __init__(
        self: base, data: _dtype, on_update: typing.Callable[[], None]
    ) -> None:
        self.__data = data
        self.__on_update = on_update

    def __resolve(
        self: base, name: str
    ) -> tuple[type, typing.Callable[[], typing.Any]]:
        try:
            cls = self.__annotations__[name]
        except KeyError:
            try:
                default = super().__getattribute__(name)
            except AttributeError:
                raise AttributeError(name=name, obj=self)
            else:
                cls: type = type(default)
                lazy_default = lambda: default
        else:
            try:
                default = super().__getattribute__(name)
            except AttributeError:
                lazy_default = lambda: cls()
            else:
                if not isinstance(default, cls):
                    raise TypeError(
                        f"Default value for {self.__class__.__name__}.{name} has incorrect type {type(default).__name__} (expected {cls.__name__})"
                    )
                lazy_default = lambda: default
        return cls, lazy_default

    def __getattribute__(self: base, name: str) -> typing.Any:
        if name.startswith("_"):
            return super().__getattribute__(name)
        cls, lazy_default = self.__resolve(name)
        if issubclass(cls, base):
            try:
                value = self.__data[name]
            except KeyError:
                value = None
            if not isinstance(value, dict):
                value = {}
                self.__data[name] = value
            return cls(value, self.__on_update)
        else:
            try:
                value = self.__data[name]
            except KeyError:
                pass
            else:
                if isinstance(value, str):
                    return cls.__call__(value)
            return lazy_default()

    def __setattr__(self: base, name: str, value: typing.Any) -> None:
        if name.startswith("_"):
            super().__setattr__(name, value)
            return
        cls, _ = self.__resolve(name)
        if issubclass(cls, base):
            raise AttributeError(name=name, obj=self)
        if not isinstance(value, cls):
            raise TypeError(
                f"Assigned value for {self.__class__.__name__}.{name} has incorrect type {type(value).__name__} (expected {cls.__name__})"
            )
        self.__data[name] = str(value)
        self.__on_update()

    def __delattr__(self: base, name: str) -> None:
        if name.startswith("_"):
            super().__delattr__(name)
            return
        del self.__data[name]
        self.__on_update()
