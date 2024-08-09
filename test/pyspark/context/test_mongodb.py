from unittest.mock import sentinel

from glue_utils.pyspark import (
    ConnectionType,
    GluePySparkContext,
)


class TestGluePySparkContextForMongoDB:
    def test_create_dynamic_frame(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_create_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.create_dynamic_frame_from_mongodb(
            connection_options={
                "connectionName": "connectionName",
                "database": "mongodbName",
                "collection": "mongodbCollection",
                "partitioner": "com.mongodb.spark.sql.connector.read.partitioner.SinglePartitionPartitioner",
                "partitionerOptions.partitionSizeMB": "10",
                "partitionerOptions.partitionKey": "_id",
                "disableUpdateUri": "false",
            },
            transformation_ctx="test",
        )

        mock_create_dynamic_frame_from_options.assert_called_once_with(
            connection_type=ConnectionType.MONGODB.value,
            connection_options={
                "connectionName": "connectionName",
                "database": "mongodbName",
                "collection": "mongodbCollection",
                "partitioner": "com.mongodb.spark.sql.connector.read.partitioner.SinglePartitionPartitioner",
                "partitionerOptions.partitionSizeMB": "10",
                "partitionerOptions.partitionKey": "_id",
                "disableUpdateUri": "false",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    def test_write_dynamic_frame(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_write_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.write_dynamic_frame_to_mongodb(
            frame=sentinel.dynamic_frame,
            connection_options={
                "connectionName": "connectionName",
                "database": "mongodbName",
                "collection": "mongodbCollection",
                "disableUpdateUri": "false",
                "retryWrites": "false",
            },
            transformation_ctx="test",
        )

        mock_write_dynamic_frame_from_options.assert_called_once_with(
            frame=sentinel.dynamic_frame,
            connection_type=ConnectionType.MONGODB.value,
            connection_options={
                "connectionName": "connectionName",
                "database": "mongodbName",
                "collection": "mongodbCollection",
                "disableUpdateUri": "false",
                "retryWrites": "false",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame
