"""Module for conveniently parsing options resolved from command-line arguments."""

from __future__ import annotations

import sys
from dataclasses import Field, dataclass, fields
from typing import Any, get_type_hints

from awsglue.utils import getResolvedOptions
from typing_extensions import Self


class UnsupportedTypeWarning(UserWarning):
    """Warning for unsupported field types."""


class UnsupportedTypeError(TypeError):
    """Error raised when field type is not supported."""


@dataclass
class BaseOptions:
    """Dataclass for storing resolved options."""

    @classmethod
    def __init_subclass__(cls) -> None:
        """Raise error when using unsupported types."""
        for name, type_hint in get_type_hints(cls).items():
            if type_hint not in cls.SUPPORTED_TYPES:
                msg = f"Field {name} has unsupported type annotation: {type_hint}"
                raise UnsupportedTypeError(msg)
        super().__init_subclass__()

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

    def __post_init__(self) -> None:
        """Convert field values to their annotated types."""
        type_hints = get_type_hints(self)

        for field in fields(self):
            value = getattr(self, field.name)
            target_type = type_hints.get(field.name, Any)

            if not isinstance(value, target_type):
                self._convert_and_set_field_value(field, value, target_type)

    def _convert_and_set_field_value(
        self,
        field: Field[Any],
        value: Any,  # noqa: ANN401
        target_type: type,
    ) -> None:
        """Convert and set the field value to the target type."""
        if target_type not in {str, int, float, bool}:
            msg = f"Field {field.name} has unsupported type annotation: {target_type}"
            raise UnsupportedTypeError(msg)

        try:
            if target_type is bool:
                # Special handling for boolean strings
                converted = str(value).lower() in ("true", "t", "yes", "y", "1")
            else:
                converted = target_type(value)
            setattr(self, field.name, converted)
        except (ValueError, TypeError) as e:
            msg = f"Could not convert field {field.name} value '{value}' to {target_type.__name__}"
            raise ValueError(msg) from e
