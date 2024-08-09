from unittest.mock import sentinel

from glue_utils.pyspark import (
    ConnectionType,
    GluePySparkContext,
)


class TestGluePySparkContextForDynamoDB:
    def test_create_dynamic_frame(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_create_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.create_dynamic_frame_from_dynamodb(
            connection_options={
                "dynamodb.input.tableName": "test_source",
                "dynamodb.throughput.read.percent": "1.0",
                "dynamodb.splits": "100",
            },
            transformation_ctx="test",
        )

        mock_create_dynamic_frame_from_options.assert_called_once_with(
            connection_type=ConnectionType.DYNAMODB.value,
            connection_options={
                "dynamodb.input.tableName": "test_source",
                "dynamodb.throughput.read.percent": "1.0",
                "dynamodb.splits": "100",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    def test_write_dynamic_frame(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_write_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.write_dynamic_frame_to_dynamodb(
            frame=sentinel.dynamic_frame,
            connection_options={
                "dynamodb.output.tableName": "test_sink",
                "dynamodb.throughput.write.percent": "1.0",
            },
            transformation_ctx="test",
        )

        mock_write_dynamic_frame_from_options.assert_called_once_with(
            frame=sentinel.dynamic_frame,
            connection_type=ConnectionType.DYNAMODB.value,
            connection_options={
                "dynamodb.output.tableName": "test_sink",
                "dynamodb.throughput.write.percent": "1.0",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    def test_create_dynamic_frame_using_export(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_create_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.create_dynamic_frame_from_dynamodb_export(
            connection_options={
                "dynamodb.export": "ddb",
                "dynamodb.tableArn": "test_source",
                "dynamodb.s3.bucket": "bucket_name",
                "dynamodb.s3.prefix": "bucket_prefix",
                "dynamodb.s3.bucketOwner": "account_id_of_bucket",
            },
            transformation_ctx="test",
        )

        mock_create_dynamic_frame_from_options.assert_called_once_with(
            connection_type=ConnectionType.DYNAMODB.value,
            connection_options={
                "dynamodb.export": "ddb",
                "dynamodb.tableArn": "test_source",
                "dynamodb.s3.bucket": "bucket_name",
                "dynamodb.s3.prefix": "bucket_prefix",
                "dynamodb.s3.bucketOwner": "account_id_of_bucket",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame
