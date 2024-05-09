"""Module providing the GluePySparkJob class for handling Glue ETL jobs."""

from __future__ import annotations

import sys
from contextlib import contextmanager
from dataclasses import fields
from typing import TYPE_CHECKING, Generic, cast, overload

from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark import SparkContext
from typing_extensions import TypeVar

from glue_utils import BaseOptions
from glue_utils.pyspark.context import GluePySparkContext

if TYPE_CHECKING:
    from collections.abc import Generator

    from pyspark.sql import SparkSession

T = TypeVar("T", bound=BaseOptions, default=BaseOptions)


class GluePySparkJob(Generic[T]):
    """Class that handles the boilerplate setup for Glue ETL jobs."""

    options: T
    sc: SparkContext
    spark: SparkSession
    glue_context: GluePySparkContext

    @overload
    def __init__(
        self: GluePySparkJob[BaseOptions],
    ) -> None: ...

    @overload
    def __init__(
        self: GluePySparkJob[T],
        *,
        options_cls: type[T],
    ) -> None: ...

    def __init__(
        self,
        *,
        options_cls: type[T | BaseOptions] = BaseOptions,
    ) -> None:
        """Initialize the GlueETLJob.

        Parameters
        ----------
        options_cls, optional
            Has to be a subclass of BaseOptions, by default BaseOptions

        """
        if not issubclass(options_cls, BaseOptions):
            msg = "options_cls must be a subclass of BaseOptions."
            raise TypeError(msg)

        field_names = {field.name for field in fields(options_cls)}

        params = []
        if "--JOB_NAME" in sys.argv:
            params.append("JOB_NAME")
        params.extend(field_names)

        _options = getResolvedOptions(sys.argv, params)

        self.options = cast(T, options_cls.from_options(_options))

        self.sc = SparkContext.getOrCreate()
        self.glue_context = GluePySparkContext(self.sc)
        self.spark = self.glue_context.spark_session

        self._job = Job(self.glue_context)
        self._job.init(_options.get("JOB_NAME", ""), _options)

    @contextmanager
    def managed_glue_context(
        self,
        *,
        commit: bool = True,
    ) -> Generator[GluePySparkContext, None, None]:
        """Context manager for managing the GluePySparkContext.

        Parameters
        ----------
        commit, optional
            Whether to commit the job, by default True

        """
        yield self.glue_context
        if commit:
            self.commit()

    def commit(self) -> None:
        """Commit the Glue ETL job."""
        self._job.commit()
