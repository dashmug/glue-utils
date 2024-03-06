from awsglue.context import GlueContext
from glue_utils import ManagedGlueContext
from pyspark import SparkConf
from pyspark.sql import SparkSession


class TestManagedGlueContext:
    def test_init_without_options(self):
        context = ManagedGlueContext()

        assert context.options == {}

    def test_init_with_options(self):
        context = ManagedGlueContext(
            options={"JOB_NAME": "test_job", "SOME_OPTION": "some_value"},
        )

        assert context.options == {
            "JOB_NAME": "test_job",
            "SOME_OPTION": "some_value",
        }

    def test_as_context_manager(self):
        options = {"JOB_NAME": "test_job"}
        conf = SparkConf().set("Some.Dummy.Key", "Value")

        with ManagedGlueContext(options=options, conf=conf) as context:
            assert isinstance(context, GlueContext)
            assert isinstance(context.spark_session, SparkSession)
            assert context.spark_session.sparkContext.appName == "test_job"
            assert (
                context.spark_session.sparkContext.getConf().get("Some.Dummy.Key")
                == "Value"
            )
