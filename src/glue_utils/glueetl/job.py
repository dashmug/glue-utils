"""Module providing the GlueETLJob class for handling Glue ETL jobs."""

import sys
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import fields
from typing import Generic

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from typing_extensions import TypeVar

from glue_utils import BaseOptions

T = TypeVar("T", bound=BaseOptions)


class GlueETLJob(Generic[T]):
    """A class that handles the boilerplate setup for Glue ETL jobs."""

    options: T
    glue_context: GlueContext
    spark: SparkSession

    def __init__(
        self,
        *,
        options_cls: type[T] = BaseOptions,  # type: ignore[assignment]
    ) -> None:
        """Initialize the GlueETLJob."""
        job_options = getResolvedOptions(
            sys.argv,
            [field.name for field in fields(options_cls)],
        )

        self.options = options_cls.from_resolved_options(job_options)

        self.glue_context = self.create_glue_context()
        self.spark = self.glue_context.spark_session

        self._job = Job(self.glue_context)
        self._job.init(self.options.JOB_NAME, job_options)

    def create_glue_context(self) -> GlueContext:
        """Create a GlueContext.

        Override this method to customize the GlueContext creation.
        """
        spark_conf = SparkConf().setAppName(self.options.JOB_NAME)
        spark_context = SparkContext.getOrCreate(spark_conf)

        return GlueContext(spark_context)

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
