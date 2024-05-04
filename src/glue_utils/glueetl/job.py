"""Module providing the GlueETLJob class for handling Glue ETL jobs."""

from __future__ import annotations

import sys
from contextlib import contextmanager
from dataclasses import fields
from typing import TYPE_CHECKING, Generic, cast, overload

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark import SparkConf, SparkContext
from typing_extensions import TypeVar

from glue_utils import BaseOptions

if TYPE_CHECKING:
    from collections.abc import Generator

    from pyspark.sql import SparkSession

T = TypeVar("T", bound=BaseOptions, default=BaseOptions)


class GlueETLJob(Generic[T]):
    """Class that handles the boilerplate setup for Glue ETL jobs."""

    name: str
    options: T
    sc: SparkContext
    spark: SparkSession
    glue_context: GlueContext

    @overload
    def __init__(
        self: GlueETLJob[BaseOptions],
    ) -> None: ...

    @overload
    def __init__(
        self: GlueETLJob[T],
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

        params = []
        if "--JOB_NAME" in sys.argv:
            params.append("JOB_NAME")
        params.extend(field.name for field in fields(options_cls))

        job_options = getResolvedOptions(sys.argv, params)

        self.options = cast(T, options_cls.from_resolved_options(job_options))

        self.name = job_options.get("JOB_NAME", "glueetl-job")

        self.sc = self.create_spark_context()
        self.glue_context = self.create_glue_context()
        self.spark = self.glue_context.spark_session

        self._job = Job(self.glue_context)
        self._job.init(self.name, job_options)

    def create_spark_context(self) -> SparkContext:
        """Create a SparkContext.

        Override this method to customize the SparkContext creation.
        """
        spark_conf = SparkConf().setAppName(self.name)

        return SparkContext.getOrCreate(spark_conf)

    def create_glue_context(self) -> GlueContext:
        """Create a GlueContext.

        Override this method to customize the GlueContext creation.
        """
        return GlueContext(self.sc)

    @contextmanager
    def managed_glue_context(
        self,
        *,
        commit: bool = True,
    ) -> Generator[GlueContext, None, None]:
        """Context manager for managing the GlueContext.

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
