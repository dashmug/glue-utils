"""Module for conveniently parsing options resolved from command-line arguments."""

from __future__ import annotations

import sys
from dataclasses import dataclass, fields
from typing import Any

from awsglue.utils import getResolvedOptions
from typing_extensions import Self


@dataclass
class BaseOptions:
    """Dataclass for storing resolved options."""

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
