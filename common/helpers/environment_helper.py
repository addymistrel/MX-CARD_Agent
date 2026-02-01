from typing import TypeVar, overload
import os

T = TypeVar("T", str, int, float, bool)

class EnvironmentHelper:
    @overload
    @staticmethod
    def get_env_variable(name: str) -> str | None: ...

    @overload
    @staticmethod
    def get_env_variable(name: str, default: T) -> T | str: ...

    @staticmethod
    def get_env_variable(name: str, default: T | None = None) -> T | str | None:
        value = os.getenv(name)

        if value is None:
            return default

        if default is None:
            return value

        try:
            if isinstance(default, bool):
                return value.lower() in ("true", "1", "yes", "on")
            elif isinstance(default, int):
                return int(value)
            elif isinstance(default, float):
                return float(value)
            else:
                return value
        except (ValueError, AttributeError):
            return value
