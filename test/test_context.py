from awsglue.context import GlueContext
from glue_utils import ManagedGlueContext
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession


class TestManagedGlueContext:
    def assert_attributes(self, context):
        assert isinstance(context, GlueContext)
        assert isinstance(context.spark_session, SparkSession)
        assert isinstance(context.spark_session.sparkContext, SparkContext)

    def test_as_context_manager(self):
        with ManagedGlueContext() as context:
            self.assert_attributes(context=context)

            spark_context = context.spark_session.sparkContext

            assert spark_context.appName == ""
            assert spark_context.getConf().get("Test.Name") is None

        spark_context.stop()

    def test_as_context_manager_with_job_options(self):
        job_options = {"JOB_NAME": "test-job-options-only"}

        with ManagedGlueContext(
            job_options=job_options,
        ) as context:
            self.assert_attributes(context=context)

            spark_context = context.spark_session.sparkContext

            assert spark_context.appName == "test-job-options-only"
            assert spark_context.getConf().get("Test.Name") is None

        spark_context.stop()

    def test_as_context_manager_with_spark_conf(self):
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

            spark_context = context.spark_session.sparkContext

            assert spark_context.appName == "test-job-with-spark-conf"
            assert spark_context.getConf().get("Test.Name") == "With Spark Conf"

        spark_context.stop()
