"""Module for conveniently parsing options resolved from command-line arguments.

This is limited to python 3.9 since Glue PythonShell jobs only supports 3.9.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, fields
from typing import Any, get_type_hints
from warnings import warn

from awsglue.utils import getResolvedOptions
from typing_extensions import Self


class UnsupportedTypeWarning(UserWarning):
    """Warning for unsupported field types."""


@dataclass
class BaseOptions:
    """Dataclass for storing resolved options for Glue Pythonshell jobs."""

    @classmethod
    def __init_subclass__(cls) -> None:
        """Warn if fields are not strings."""
        for name, type_hint in get_type_hints(cls).items():
            if type_hint is not str:
                warn(
                    f'"{name}" value is a string at runtime even if annotated to be "{type_hint}".',
                    UnsupportedTypeWarning,
                    stacklevel=2,
                )
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
