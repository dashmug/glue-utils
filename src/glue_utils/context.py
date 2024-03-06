"""Module providing the ManagedGlueContext class for managing GlueContext."""

from contextlib import ContextDecorator
from types import TracebackType
from typing import cast

from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark import SparkConf, SparkContext
from typing_extensions import Self


class ManagedGlueContext(ContextDecorator):
    """A context manager that wraps a GlueContext.

    This context manager ensures that Job.commit() is called.
    """

    options: dict[str, str]
    conf: SparkConf | None
    job: Job

    def __init__(
        self: Self,
        *,
        options: dict[str, str] | None = None,
        conf: SparkConf | None = None,
    ) -> None:
        """Create the context manager with the given options and configuration.

        Parameters
        ----------
        options : dict[str, str] | None, optional
            Dictionary of key-value pairs to pass to Job.init(), by default None
        conf : SparkConf | None, optional
            Custom SparkConf to use with SparkContext.getOrCreate(), by default None

        """
        self.options = options or {}
        self.conf = conf

        super().__init__()

    def __enter__(self: Self) -> GlueContext:
        """Enter the context manager and return the GlueContext.

        Returns
        -------
        GlueContext
            This GlueContext object.

        """
        job_name = self.options.get("JOB_NAME", "")

        conf = self.conf or SparkConf()
        conf = conf.setAppName(job_name)

        spark_context = SparkContext.getOrCreate(conf)
        self.glue_context = GlueContext(spark_context)

        self.job = Job(self.glue_context)
        self.job.init(job_name, self.options)

        return self.glue_context

    def __exit__(
        self: Self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        """Exit the context manager and commit the job.

        Parameters
        ----------
        exc_type : type[BaseException] | None
            The type of the exception raised, if any.
        exc_value : BaseException | None
            The exception instance raised, if any.
        traceback : TracebackType | None
            The traceback of the exception raised, if any.

        Returns
        -------
        bool | None
            The return value indicating whether the exception was
            handled or not.

        """
        self.job.commit()

        return cast(bool, False)  # noqa: FBT003
