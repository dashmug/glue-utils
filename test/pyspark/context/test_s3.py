from unittest.mock import sentinel

from glue_utils.pyspark import GluePySparkContext
from glue_utils.pyspark.connection_options import (
    S3ParquetSourceConnectionOptions,
    S3SinkConnectionOptions,
    S3SourceConnectionOptions,
)
from glue_utils.pyspark.format_options import (
    CSVFormatOptions,
    JSONFormatOptions,
    ParquetFormatOptions,
    XMLFormatOptions,
)


class TestGluePySparkContextForS3:
    def test_create_dynamic_frame_from_s3_json(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_create_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.create_dynamic_frame_from_s3_json(
            connection_options=S3SourceConnectionOptions(
                paths=["s3://bucket/key/input-path"]
            ),
            format_options=JSONFormatOptions(
                jsonPath="something",
                optimizePerformance=True,
            ),
            transformation_ctx="test",
        )

        mock_create_dynamic_frame_from_options.assert_called_once_with(
            connection_type="s3",
            connection_options={"paths": ["s3://bucket/key/input-path"]},
            format="json",
            format_options={"jsonPath": "something", "optimizePerformance": True},
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    def test_create_dynamic_frame_from_s3_parquet(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_create_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.create_dynamic_frame_from_s3_parquet(
            connection_options=S3ParquetSourceConnectionOptions(
                paths=["s3://bucket/key/input-path"],
                mergeSchema=True,
            ),
            format_options=ParquetFormatOptions(compression="gzip"),
            transformation_ctx="test",
        )

        mock_create_dynamic_frame_from_options.assert_called_once_with(
            connection_type="s3",
            connection_options={
                "paths": ["s3://bucket/key/input-path"],
                "mergeSchema": True,
            },
            format="parquet",
            format_options={"compression": "gzip"},
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    def test_create_dynamic_frame_from_s3_csv(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_create_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.create_dynamic_frame_from_s3_csv(
            connection_options=S3SourceConnectionOptions(
                paths=["s3://bucket/key/input-path"]
            ),
            format_options=CSVFormatOptions(
                withHeader=True,
                optimizePerformance=True,
                quoteChar=-1,
            ),
            transformation_ctx="test",
        )

        mock_create_dynamic_frame_from_options.assert_called_once_with(
            connection_type="s3",
            connection_options={"paths": ["s3://bucket/key/input-path"]},
            format="csv",
            format_options={
                "withHeader": True,
                "optimizePerformance": True,
                "quoteChar": -1,
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    def test_create_dynamic_frame_from_s3_xml(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_create_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.create_dynamic_frame_from_s3_xml(
            connection_options=S3SourceConnectionOptions(
                paths=["s3://bucket/key/input-path"]
            ),
            format_options=XMLFormatOptions(
                rowTag="xmlTag",
                ignoreSurroundingSpaces=True,
            ),
            transformation_ctx="test",
        )

        mock_create_dynamic_frame_from_options.assert_called_once_with(
            connection_type="s3",
            connection_options={"paths": ["s3://bucket/key/input-path"]},
            format="xml",
            format_options={"rowTag": "xmlTag", "ignoreSurroundingSpaces": True},
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    def test_write_dynamic_frame_to_s3_json(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_write_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.write_dynamic_frame_to_s3_json(
            frame=sentinel.dynamic_frame,
            connection_options=S3SinkConnectionOptions(
                path="s3://bucket/key/output-path"
            ),
            transformation_ctx="test",
        )

        mock_write_dynamic_frame_from_options.assert_called_once_with(
            frame=sentinel.dynamic_frame,
            connection_type="s3",
            connection_options={"path": "s3://bucket/key/output-path"},
            format="json",
            format_options={},
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    def test_write_dynamic_frame_to_s3_parquet(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_write_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.write_dynamic_frame_to_s3_parquet(
            frame=sentinel.dynamic_frame,
            connection_options=S3SinkConnectionOptions(
                path="s3://bucket/key/output-path"
            ),
            format_options=ParquetFormatOptions(
                useGlueParquetWriter=True,
                compression="gzip",
            ),
            transformation_ctx="test",
        )

        mock_write_dynamic_frame_from_options.assert_called_once_with(
            frame=sentinel.dynamic_frame,
            connection_type="s3",
            connection_options={"path": "s3://bucket/key/output-path"},
            format="parquet",
            format_options={"useGlueParquetWriter": True, "compression": "gzip"},
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    def test_write_dynamic_frame_to_s3_csv(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_write_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.write_dynamic_frame_to_s3_csv(
            frame=sentinel.dynamic_frame,
            connection_options=S3SinkConnectionOptions(
                path="s3://bucket/key/output-path"
            ),
            format_options=CSVFormatOptions(
                writeHeader=True,
                strictCheckForQuoting=True,
            ),
            transformation_ctx="test",
        )

        mock_write_dynamic_frame_from_options.assert_called_once_with(
            frame=sentinel.dynamic_frame,
            connection_type="s3",
            connection_options={"path": "s3://bucket/key/output-path"},
            format="csv",
            format_options={"writeHeader": True, "strictCheckForQuoting": True},
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    def test_write_dynamic_frame_to_s3_xml(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_write_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.write_dynamic_frame_to_s3_xml(
            frame=sentinel.dynamic_frame,
            connection_options=S3SinkConnectionOptions(
                path="s3://bucket/key/output-path"
            ),
            transformation_ctx="test",
        )

        mock_write_dynamic_frame_from_options.assert_called_once_with(
            frame=sentinel.dynamic_frame,
            connection_type="s3",
            connection_options={"path": "s3://bucket/key/output-path"},
            format="xml",
            format_options={},
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame
