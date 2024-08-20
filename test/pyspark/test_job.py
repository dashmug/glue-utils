from dataclasses import dataclass, fields
from typing import TYPE_CHECKING
from unittest.mock import ANY, patch

import pytest
from awsglue.context import GlueContext
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from typing_extensions import TypeVar

from glue_utils import BaseOptions
from glue_utils.pyspark import GluePySparkJob

if TYPE_CHECKING:
    from glue_utils.pyspark import GlueContextOptions


@dataclass
class MockOptions(BaseOptions):
    OPTION_FROM_CLASS_A: str
    OPTION_FROM_CLASS_B: str = "default-value"


class Dummy: ...


@pytest.fixture
def mock_get_resolved_options():
    with patch("glue_utils.pyspark.job.getResolvedOptions") as patched:
        yield patched


@pytest.fixture
def mock_glue_pyspark_context_cls():
    with patch("glue_utils.pyspark.job.GluePySparkContext") as patched:
        yield patched


@pytest.fixture
def mock_job():
    with patch("glue_utils.pyspark.job.Job") as patched:
        yield patched.return_value


@pytest.fixture
def glue_pyspark_job(mock_get_resolved_options):
    mock_get_resolved_options.return_value = {
        "JOB_NAME": "test-job",
    }

    job = GluePySparkJob()
    yield job
    job.sc.stop()


def assert_glue_context_attributes(glue_context: GlueContext) -> None:
    assert isinstance(glue_context, GlueContext)
    assert isinstance(glue_context.spark_session, SparkSession)
    assert isinstance(glue_context.spark_session.sparkContext, SparkContext)


T = TypeVar("T", bound=BaseOptions, default=BaseOptions)


def assert_job_attributes(job: GluePySparkJob[T]) -> None:
    sc = job.sc
    glue_context = job.glue_context

    assert isinstance(sc, SparkContext)
    assert_glue_context_attributes(glue_context)
    assert job.sc == glue_context.spark_session.sparkContext


class TestGluePySparkJob:
    @pytest.mark.parametrize(
        ("args", "resolved_options"),
        [
            (
                ["--JOB_NAME", "test-job"],
                {"JOB_NAME": "test-job"},
            ),
            ([], {}),
        ],
    )
    def test_init(
        self, args, resolved_options, mock_get_resolved_options, mock_job
    ) -> None:
        mock_get_resolved_options.return_value = resolved_options

        with patch("sys.argv", ["test.py", *args]):
            job = GluePySparkJob()

            mock_get_resolved_options.assert_called_once()

            assert len(fields(job.options)) == 0

            assert_job_attributes(job)

            mock_job.init.assert_called_once_with(
                resolved_options.get("JOB_NAME", ""),
                resolved_options,
            )

            job.sc.stop()

    def test_init_options_cls(self, mock_get_resolved_options, mock_job) -> None:
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
            "OPTION_FROM_CLASS_A": "mock-option",
        }

        job = GluePySparkJob(options_cls=MockOptions)

        mock_get_resolved_options.assert_called_once()

        assert job.options.OPTION_FROM_CLASS_A == "mock-option"
        assert job.options.OPTION_FROM_CLASS_B == "default-value"
        assert len(fields(job.options)) == 2

        assert_job_attributes(job)

        mock_job.init.assert_called_once_with(
            "test-job",
            {
                "JOB_NAME": "test-job",
                "OPTION_FROM_CLASS_A": "mock-option",
            },
        )

        job.sc.stop()

    def test_init_with_invalid_options_cls(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
            "OPTION_FROM_CLASS_A": "mock-option",
        }

        with pytest.raises(
            TypeError,
            match="options_cls must be a subclass of BaseOptions",
        ):
            GluePySparkJob(options_cls=Dummy)  # type: ignore[type-var]

    def test_init_with_invalid_spark_conf(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
        }

        with pytest.raises(TypeError, match="conf must be an instance of SparkConf"):
            GluePySparkJob(spark_conf=Dummy())  # type: ignore[call-overload]

    def test_init_with_spark_conf(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
        }

        spark_conf = SparkConf()
        spark_conf.set("test.key", "test.value")

        job = GluePySparkJob(spark_conf=spark_conf)

        assert_job_attributes(job)
        assert job.sc.getConf().get("test.key") == "test.value"

        job.sc.stop()

    def test_init_with_partition_options(
        self,
        mock_get_resolved_options,
        mock_glue_pyspark_context_cls,
    ) -> None:
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
        }

        glue_context_options: GlueContextOptions = {
            "minPartitions": 2,
            "targetPartitions": 2,
        }

        job = GluePySparkJob(glue_context_options=glue_context_options)

        mock_glue_pyspark_context_cls.assert_called_once_with(
            ANY,
            minPartitions=2,
            targetPartitions=2,
        )
        assert isinstance(job.sc, SparkContext)

        job.sc.stop()

    @pytest.mark.parametrize("level", list(GluePySparkJob.LogLevel))
    @patch("glue_utils.pyspark.job.SparkContext")
    def test_init_with_log_level(
        self,
        mock_spark_context_cls,
        level,
        mock_get_resolved_options,
        mock_glue_pyspark_context_cls,
    ) -> None:
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
        }

        GluePySparkJob(log_level=level)

        mock_glue_pyspark_context_cls.assert_called_once_with(ANY)
        mock_spark_context_cls.getOrCreate.return_value.setLogLevel.assert_called_once_with(
            level.value
        )

    @patch("glue_utils.pyspark.job.SparkContext")
    def test_init_with_default_log_level(
        self,
        mock_spark_context_cls,
        mock_get_resolved_options,
        mock_glue_pyspark_context_cls,
    ) -> None:
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
        }

        GluePySparkJob()

        mock_glue_pyspark_context_cls.assert_called_once_with(ANY)
        mock_spark_context_cls.getOrCreate.return_value.setLogLevel.assert_called_once_with(
            GluePySparkJob.LogLevel.WARN.value
        )


class TestGluePySparkJobMethods:
    def test_managed_glue_context(self, mock_job, glue_pyspark_job) -> None:
        with glue_pyspark_job.managed_glue_context() as glue_context:
            assert_glue_context_attributes(glue_context)

        mock_job.commit.assert_called_once()

    def test_managed_glue_context_without_commit(
        self, mock_job, glue_pyspark_job
    ) -> None:
        with glue_pyspark_job.managed_glue_context(commit=False) as glue_context:
            assert_glue_context_attributes(glue_context)

        mock_job.commit.assert_not_called()

    def test_commit(self, mock_job, glue_pyspark_job) -> None:
        glue_pyspark_job.commit()

        mock_job.commit.assert_called_once()
