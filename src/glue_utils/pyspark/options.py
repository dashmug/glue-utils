"""Module for conveniently parsing options resolved from command-line arguments."""

from __future__ import annotations

import sys
from dataclasses import dataclass, fields
from typing import Any, ClassVar, get_args, get_origin, get_type_hints

from awsglue.utils import getResolvedOptions
from typing_extensions import Self


class UnsupportedTypeError(TypeError):
    """Error raised when field type is not supported for conversion."""

    def __init__(self, target_type: type) -> None:
        """Initialize with unsupported type."""
        msg = f"Unsupported type annotation: {target_type}"
        super().__init__(msg)


@dataclass
class BaseOptions:
    """Dataclass for storing resolved options with type conversion support."""

    # Class variables for boolean conversion - can be overridden in subclasses
    TRUE_VALUES: ClassVar[set[str]] = {"1", "true", "yes", "y", "t"}
    FALSE_VALUES: ClassVar[set[str]] = {"0", "false", "no", "n", "f"}

    def __post_init__(self) -> None:
        """Convert string values to their annotated types after initialization."""
        type_hints = get_type_hints(self.__class__)
        for field in fields(self):
            value = getattr(self, field.name)
            target_type = type_hints.get(field.name, str)
            real_type = self._resolve_real_type(target_type, value)
            if value is not None and not isinstance(value, real_type):
                try:
                    converted = self.convert_value(value, real_type)
                    setattr(self, field.name, converted)
                except Exception as e:
                    msg = f"Failed to convert field '{field.name}' value '{value}' to {real_type}: {e}"
                    raise ValueError(msg) from e

    def convert_value(self, value: object, target_type: type) -> object:
        """Convert value to the target_type, supporting str, int, float, bool."""
        if target_type is str:
            return str(value)
        if target_type is int:
            return int(str(value))
        if target_type is float:
            return float(str(value))
        if target_type is bool:
            return self.convert_to_bool(value)
        raise UnsupportedTypeError(target_type)

    def convert_to_bool(self, value: object) -> bool:
        """Convert value to bool with special string handling."""
        if isinstance(value, bool):
            return value
        val = str(value).strip().lower()
        if val in self.TRUE_VALUES:
            return True
        if val in self.FALSE_VALUES:
            return False
        msg = f"Cannot convert '{value}' to bool."
        raise ValueError(msg)

    @classmethod
    def from_sys_argv(cls) -> Self:
        """Create an instance of the class from Glue's resolved arguments."""
        resolved_options = getResolvedOptions(
            sys.argv, [field.name for field in fields(cls)]
        )

        return cls.from_options(resolved_options)

    @classmethod
    def from_options(cls, options: dict[str, Any] | None = None) -> Self:
        """Create an instance of the class from the provided options."""
        if not options:
            return cls()

        field_names = {field.name for field in fields(cls)}

        return cls(
            **{key: value for key, value in options.items() if key in field_names},
        )

    @staticmethod
    def _resolve_real_type(target_type: type, value: object) -> type:
        """Resolve the real type for Optional/Union annotations."""
        origin = get_origin(target_type)
        args = get_args(target_type)

        if origin is None or not args:
            return target_type

        return BaseOptions._resolve_union_type(args, value)

    @staticmethod
    def _resolve_union_type(args: tuple[Any, ...], value: object) -> type:
        """Resolve the actual type from Union/Optional type arguments."""
        non_none_types = BaseOptions._extract_non_none_types(args)

        if BaseOptions._should_use_value_type(non_none_types, value):
            return type(value) if value is not None else str

        return BaseOptions._get_first_valid_type(non_none_types)

    @staticmethod
    def _extract_non_none_types(args: tuple[Any, ...]) -> tuple[Any, ...]:
        """Extract non-None types from Union/Optional arguments."""
        return tuple(t for t in args if t is not type(None))

    @staticmethod
    def _should_use_value_type(non_none_types: tuple[Any, ...], value: object) -> bool:
        """Check if we should use the value's type instead of annotation."""
        return not non_none_types or value is None

    @staticmethod
    def _get_first_valid_type(non_none_types: tuple[Any, ...]) -> type:
        """Get the first valid type from non-None types, defaulting to str."""
        if not non_none_types:
            return str
        real_type = non_none_types[0]
        return real_type if isinstance(real_type, type) else str
