"""Module for conveniently parsing options resolved from command-line arguments."""

from dataclasses import dataclass, fields
from typing import Any

from typing_extensions import Self


@dataclass(frozen=True)
class BaseOptions:
    """Dataclass for storing resolved options."""

    JOB_NAME: str

    @classmethod
    def from_resolved_options(
        cls,
        resolved_options: dict[str, Any] | None = None,
    ) -> Self:
        """Create an instance of the class from Glue's resolved options."""
        default_job_name = ""

        if not resolved_options:
            return cls(JOB_NAME=default_job_name)

        resolved_options["JOB_NAME"] = resolved_options.get(
            "JOB_NAME", default_job_name
        )

        field_names = {field.name for field in fields(cls)}

        return cls(
            **{
                key: value
                for key, value in resolved_options.items()
                if key in field_names
            }
        )
