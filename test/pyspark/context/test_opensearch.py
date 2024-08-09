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
        dynamic_frame = glue_pyspark_context.create_dynamic_frame_from_opensearch(
            connection_options={
                "connectionName": "connectionName",
                "opensearch.resource": "aosIndex",
                "pushdown": "true",
            },
            transformation_ctx="test",
        )

        mock_create_dynamic_frame_from_options.assert_called_once_with(
            connection_type=ConnectionType.OPENSEARCH.value,
            connection_options={
                "connectionName": "connectionName",
                "opensearch.resource": "aosIndex",
                "pushdown": "true",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    def test_write_dynamic_frame(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_write_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.write_dynamic_frame_to_opensearch(
            frame=sentinel.dynamic_frame,
            connection_options={
                "connectionName": "connectionName",
                "opensearch.resource": "aosIndex",
            },
            transformation_ctx="test",
        )

        mock_write_dynamic_frame_from_options.assert_called_once_with(
            frame=sentinel.dynamic_frame,
            connection_type=ConnectionType.OPENSEARCH.value,
            connection_options={
                "connectionName": "connectionName",
                "opensearch.resource": "aosIndex",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame
