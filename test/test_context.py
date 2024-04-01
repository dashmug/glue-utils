from unittest.mock import patch

import pytest
from awsglue.context import GlueContext
from glue_utils import ManagedGlueContext
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession


@pytest.fixture
def mock_job():
    with patch("glue_utils.context.Job") as mocked:
        yield mocked


class TestManagedGlueContext:
    def test_as_context_manager(self, mock_job):
        with ManagedGlueContext() as context:
            self.assert_attributes(context=context)
            mock_job.return_value.init.assert_called_once_with("", {})

            spark_context = context.spark_session.sparkContext

            assert spark_context.appName == ""
            assert spark_context.getConf().get("Test.Name") is None

        spark_context.stop()
        mock_job.return_value.commit.assert_called_once()

    def test_as_context_manager_with_job_options(self, mock_job):
        job_options = {"JOB_NAME": "test-job-options-only"}

        with ManagedGlueContext(
            job_options=job_options,
        ) as context:
            self.assert_attributes(context=context)
            mock_job.return_value.init.assert_called_once_with(
                "test-job-options-only", {"JOB_NAME": "test-job-options-only"}
            )

            spark_context = context.spark_session.sparkContext

            assert spark_context.appName == "test-job-options-only"
            assert spark_context.getConf().get("Test.Name") is None

        spark_context.stop()
        mock_job.return_value.commit.assert_called_once()

    def test_as_context_manager_with_spark_conf(self, mock_job):
        job_options = {"JOB_NAME": "test-job-with-spark-conf"}
        spark_conf = (
            SparkConf()
            .setAppName(job_options["JOB_NAME"])
            .set("Test.Name", "With Spark Conf")
        )

        with ManagedGlueContext(
            job_options=job_options,
            spark_conf=spark_conf,
        ) as context:
            self.assert_attributes(context=context)
            mock_job.return_value.init.assert_called_once_with(
                "test-job-with-spark-conf", {"JOB_NAME": "test-job-with-spark-conf"}
            )

            spark_context = context.spark_session.sparkContext

            assert spark_context.appName == "test-job-with-spark-conf"
            assert spark_context.getConf().get("Test.Name") == "With Spark Conf"

        spark_context.stop()
        mock_job.return_value.commit.assert_called_once()

    def assert_attributes(self, context):
        assert isinstance(context, GlueContext)
        assert isinstance(context.spark_session, SparkSession)
        assert isinstance(context.spark_session.sparkContext, SparkContext)
