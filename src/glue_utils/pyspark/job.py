"""Module providing the GluePySparkJob class for handling Glue ETL jobs."""

from __future__ import annotations

import sys
from contextlib import contextmanager
from dataclasses import fields
from enum import Enum
from typing import TYPE_CHECKING, Generic, cast, overload

from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark import SparkConf, SparkContext
from typing_extensions import TypeVar

from glue_utils import BaseOptions

from .context import GlueContextOptions, GluePySparkContext

if TYPE_CHECKING:
    from collections.abc import Generator

    from pyspark.sql import SparkSession

T = TypeVar("T", bound=BaseOptions, default=BaseOptions)


class GluePySparkJob(Generic[T]):
    """Class that handles the boilerplate setup for Glue ETL jobs."""

    class LogLevel(Enum):
        """Enum class representing different log levels.

        Attributes
        ----------
            ALL (str): The lowest log level, includes all log messages.
            DEBUG (str): Log level for debugging information.
            ERROR (str): Log level for error messages.
            FATAL (str): Log level for fatal error messages.
            INFO (str): Log level for informational messages.
            OFF (str): The highest log level, turns off all log messages.
            TRACE (str): Log level for detailed trace messages.
            WARN (str): Log level for warning messages.

        """

        ALL = "ALL"
        DEBUG = "DEBUG"
        ERROR = "ERROR"
        FATAL = "FATAL"
        INFO = "INFO"
        OFF = "OFF"
        TRACE = "TRACE"
        WARN = "WARN"

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
        self: GluePySparkJob[BaseOptions],
        *,
        spark_conf: SparkConf,
    ) -> None: ...

    @overload
    def __init__(
        self: GluePySparkJob[BaseOptions],
        *,
        glue_context_options: GlueContextOptions,
    ) -> None: ...

    @overload
    def __init__(
        self: GluePySparkJob[BaseOptions],
        *,
        log_level: LogLevel,
    ) -> None: ...

    @overload
    def __init__(
        self: GluePySparkJob[BaseOptions],
        *,
        spark_conf: SparkConf,
        glue_context_options: GlueContextOptions,
    ) -> None: ...

    @overload
    def __init__(
        self: GluePySparkJob[BaseOptions],
        *,
        spark_conf: SparkConf,
        log_level: LogLevel,
    ) -> None: ...

    @overload
    def __init__(
        self: GluePySparkJob[BaseOptions],
        *,
        glue_context_options: GlueContextOptions,
        log_level: LogLevel,
    ) -> None: ...

    @overload
    def __init__(
        self: GluePySparkJob[BaseOptions],
        *,
        spark_conf: SparkConf,
        glue_context_options: GlueContextOptions,
        log_level: LogLevel,
    ) -> None: ...

    @overload
    def __init__(
        self: GluePySparkJob[T],
        *,
        options_cls: type[T],
    ) -> None: ...

    @overload
    def __init__(
        self: GluePySparkJob[T],
        *,
        options_cls: type[T],
        spark_conf: SparkConf,
    ) -> None: ...

    @overload
    def __init__(
        self: GluePySparkJob[T],
        *,
        options_cls: type[T],
        glue_context_options: GlueContextOptions,
    ) -> None: ...

    @overload
    def __init__(
        self: GluePySparkJob[T],
        *,
        options_cls: type[T],
        log_level: LogLevel,
    ) -> None: ...

    @overload
    def __init__(
        self: GluePySparkJob[T],
        *,
        options_cls: type[T],
        spark_conf: SparkConf,
        glue_context_options: GlueContextOptions,
    ) -> None: ...

    @overload
    def __init__(
        self: GluePySparkJob[T],
        *,
        options_cls: type[T],
        spark_conf: SparkConf,
        log_level: LogLevel,
    ) -> None: ...

    @overload
    def __init__(
        self: GluePySparkJob[T],
        *,
        options_cls: type[T],
        glue_context_options: GlueContextOptions,
        log_level: LogLevel,
    ) -> None: ...

    @overload
    def __init__(
        self: GluePySparkJob[T],
        *,
        options_cls: type[T],
        spark_conf: SparkConf,
        glue_context_options: GlueContextOptions,
        log_level: LogLevel,
    ) -> None: ...

    def __init__(
        self,
        *,
        options_cls: type[T | BaseOptions] = BaseOptions,
        spark_conf: SparkConf | None = None,
        glue_context_options: GlueContextOptions | None = None,
        log_level: LogLevel = LogLevel.WARN,
    ) -> None:
        """Initialize a Job object.

        Parameters
        ----------
        options_cls : type[T | BaseOptions], optional
            The class representing the options for the job. Defaults to
            BaseOptions.
        spark_conf : SparkConf | None, optional
            The Spark configuration. Defaults to None.
        glue_context_options : GlueContextOptions | None, optional
            The Glue context options. Defaults to None.
        log_level : LogLevel, optional
            The log level for the job. Defaults to LogLevel.WARN.

        """
        if not issubclass(options_cls, BaseOptions):
            msg = "options_cls must be a subclass of BaseOptions."
            raise TypeError(msg)

        field_names = {field.name for field in fields(options_cls)}

        params = []
        if "--JOB_NAME" in sys.argv:
            params.append("JOB_NAME")
        params.extend(field_names)

        glue_args = getResolvedOptions(sys.argv, params)

        self.options = cast("T", options_cls.from_options(glue_args))

        self.sc = self.create_spark_context(spark_conf)
        self.set_log_level(log_level)

        self.glue_context = self.create_glue_context(glue_context_options)
        self.spark = self.glue_context.spark_session

        self._job = Job(self.glue_context)
        self._job.init(glue_args.get("JOB_NAME", ""), glue_args)

    def create_spark_context(self, conf: SparkConf | None = None) -> SparkContext:
        """Create a SparkContext.

        Parameters
        ----------
        conf, optional
            The SparkConf to use, by default None

        Returns
        -------
        SparkContext
            The SparkContext created.

        """
        if conf:
            if not isinstance(conf, SparkConf):
                msg = "conf must be an instance of SparkConf."
                raise TypeError(msg)
            return SparkContext.getOrCreate(conf=conf)
        return SparkContext.getOrCreate()

    def create_glue_context(
        self,
        glue_context_options: GlueContextOptions | None = None,
    ) -> GluePySparkContext:
        """Create a GluePySparkContext object using the provided SparkContext and PartitionOptions.

        Parameters
        ----------
        glue_context_options : GlueContextOptions | None, optional
            Optional PartitionOptions object containing additional
            options for configuring the GlueContext.

        """
        if glue_context_options:
            return GluePySparkContext(self.sc, **glue_context_options)
        return GluePySparkContext(self.sc)

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

    def set_log_level(
        self,
        level: LogLevel,
    ) -> None:
        """Set the log level for the SparkContext.

        Parameters
        ----------
        level : LogLevel
            The log level to be set.

        """
        self.sc.setLogLevel(level.value)
