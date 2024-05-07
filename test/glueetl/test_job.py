from dataclasses import dataclass, fields
from unittest.mock import patch

import pytest
from awsglue.context import GlueContext
from glue_utils import BaseOptions
from glue_utils.glueetl import GlueETLJob
from pyspark import SparkContext
from pyspark.sql import SparkSession
from typing_extensions import TypeVar


@dataclass
class MockOptions(BaseOptions):
    OPTION_FROM_CLASS_A: str
    OPTION_FROM_CLASS_B: str = "default-value"


class NotBaseOptions: ...


@pytest.fixture
def mock_get_resolved_options():
    with patch("glue_utils.glueetl.job.getResolvedOptions") as patched:
        yield patched


@pytest.fixture
def mock_job():
    with patch("glue_utils.glueetl.job.Job") as patched:
        yield patched.return_value


@pytest.fixture
def glueetl_job(mock_get_resolved_options):
    mock_get_resolved_options.return_value = {
        "JOB_NAME": "test-job",
    }

    job = GlueETLJob()

    yield job

    job.sc.stop()


def assert_glue_context_attributes(glue_context: GlueContext):
    assert isinstance(glue_context, GlueContext)
    assert isinstance(glue_context.spark_session, SparkSession)
    assert isinstance(glue_context.spark_session.sparkContext, SparkContext)


T = TypeVar("T", bound=BaseOptions, default=BaseOptions)


def assert_job_attributes(job: GlueETLJob[T]):
    sc = job.sc

    assert isinstance(sc, SparkContext)

    glue_context = job.glue_context

    assert_glue_context_attributes(glue_context)

    assert job.sc == glue_context.spark_session.sparkContext


class TestGlueETLJob:
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
    def test_init(self, args, resolved_options, mock_get_resolved_options, mock_job):
        mock_get_resolved_options.return_value = resolved_options

        with patch("sys.argv", ["test.py", *args]):
            job = GlueETLJob()

            mock_get_resolved_options.assert_called_once()

            assert len(fields(job.options)) == 0

            assert_job_attributes(job)

            mock_job.init.assert_called_once_with(
                resolved_options.get("JOB_NAME", ""),
                resolved_options,
            )

    def test_init_options_cls(self, mock_get_resolved_options, mock_job):
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
            "OPTION_FROM_CLASS_A": "mock-option",
        }

        job = GlueETLJob(options_cls=MockOptions)

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

    def test_init_with_invalid_options_cls(self, mock_get_resolved_options):
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
            "OPTION_FROM_CLASS_A": "mock-option",
        }

        with pytest.raises(TypeError):
            GlueETLJob(options_cls=NotBaseOptions)  # type: ignore[type-var]

    def test_managed_glue_context(self, mock_job, glueetl_job):
        with glueetl_job.managed_glue_context() as glue_context:
            assert_glue_context_attributes(glue_context)

        mock_job.commit.assert_called_once()

    def test_managed_glue_context_without_commit(self, mock_job, glueetl_job):
        with glueetl_job.managed_glue_context(commit=False) as glue_context:
            assert_glue_context_attributes(glue_context)

        mock_job.commit.assert_not_called()

    def test_commit(self, mock_job, glueetl_job):
        glueetl_job.commit()

        mock_job.commit.assert_called_once()
