from unittest.mock import sentinel

from glue_utils.pyspark import (
    ConnectionType,
    GluePySparkContext,
)


class TestGluePySparkContextForDocumentDB:
    def test_create_dynamic_frame(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_create_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.create_dynamic_frame_from_documentdb(
            connection_options={
                "uri": "documentdb_uri",
                "database": "test",
                "collection": "coll",
                "username": "username",
                "password": "1234567890",
                "ssl": "true",
                "ssl.domain_match": "false",
                "partitioner": "MongoSamplePartitioner",
                "partitionerOptions.partitionSizeMB": "10",
                "partitionerOptions.partitionKey": "_id",
            },
            transformation_ctx="test",
        )

        mock_create_dynamic_frame_from_options.assert_called_once_with(
            connection_type=ConnectionType.DOCUMENTDB.value,
            connection_options={
                "uri": "documentdb_uri",
                "database": "test",
                "collection": "coll",
                "username": "username",
                "password": "1234567890",
                "ssl": "true",
                "ssl.domain_match": "false",
                "partitioner": "MongoSamplePartitioner",
                "partitionerOptions.partitionSizeMB": "10",
                "partitionerOptions.partitionKey": "_id",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    def test_write_dynamic_frame(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_write_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.write_dynamic_frame_to_documentdb(
            frame=sentinel.dynamic_frame,
            connection_options={
                "retryWrites": "false",
                "uri": "documentdb_write_uri",
                "database": "test",
                "collection": "coll",
                "username": "username",
                "password": "pwd",
            },
            transformation_ctx="test",
        )

        mock_write_dynamic_frame_from_options.assert_called_once_with(
            frame=sentinel.dynamic_frame,
            connection_type=ConnectionType.DOCUMENTDB.value,
            connection_options={
                "retryWrites": "false",
                "uri": "documentdb_write_uri",
                "database": "test",
                "collection": "coll",
                "username": "username",
                "password": "pwd",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame
