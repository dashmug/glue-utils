from unittest.mock import sentinel

import pytest
from glue_utils.pyspark import (
    CSVFormatOptions,
    GluePySparkContext,
    JSONFormatOptions,
    ParquetFormatOptions,
    S3FormatOptions,
    S3SinkConnectionOptions,
    S3SourceConnectionOptions,
    XMLFormatOptions,
)


class TestGluePySparkContextForS3:
    @pytest.mark.parametrize(
        ["format_name", "format_options_cls", "format_options"],
        [
            (
                "json",
                JSONFormatOptions,
                {"jsonPath": "something", "optimizePerformance": True},
            ),
            ("parquet", ParquetFormatOptions, {"compression": "gzip"}),
            (
                "csv",
                CSVFormatOptions,
                {"withHeader": True, "optimizePerformance": True},
            ),
            (
                "xml",
                XMLFormatOptions,
                {"rowTag": "xmlTag", "ignoreSurroundingSpaces": True},
            ),
        ],
    )
    def test_create_dynamic_frame_from_s3(
        self,
        format_name: str,
        format_options_cls: type[S3FormatOptions],
        format_options: dict[str, str],
        glue_pyspark_context: GluePySparkContext,
        mock_create_dynamic_frame_from_options,
    ):
        create_dynamic_frame = getattr(
            glue_pyspark_context,
            f"create_dynamic_frame_from_s3_{format_name}",
        )
        dynamic_frame = create_dynamic_frame(
            connection_options=S3SourceConnectionOptions(
                paths=["s3://bucket/key/input-path"]
            ),
            format_options=format_options_cls(**format_options)
            if format_options
            else {},
            transformation_ctx="test",
        )

        mock_create_dynamic_frame_from_options.assert_called_once_with(
            connection_type="s3",
            connection_options={"paths": ["s3://bucket/key/input-path"]},
            format=format_name,
            format_options=format_options or {},
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    @pytest.mark.parametrize(
        ["format_name", "format_options_cls", "format_options"],
        [
            (
                "json",
                JSONFormatOptions,
                None,
            ),
            (
                "parquet",
                ParquetFormatOptions,
                {"useGlueParquetWriter": True, "compression": "gzip"},
            ),
            (
                "csv",
                CSVFormatOptions,
                {"writeHeader": True, "strictCheckForQuoting": True},
            ),
            (
                "xml",
                XMLFormatOptions,
                None,
            ),
        ],
    )
    def test_write_dynamic_frame_to_s3(
        self,
        format_name: str,
        format_options_cls: type[S3FormatOptions],
        format_options: dict[str, str],
        glue_pyspark_context: GluePySparkContext,
        mock_write_dynamic_frame_from_options,
    ):
        write_dynamic_frame = getattr(
            glue_pyspark_context, f"write_dynamic_frame_to_s3_{format_name}"
        )
        dynamic_frame = write_dynamic_frame(
            frame=sentinel.dynamic_frame,
            connection_options=S3SinkConnectionOptions(
                path="s3://bucket/key/output-path"
            ),
            format_options=format_options_cls(**format_options)
            if format_options
            else {},
            transformation_ctx="test",
        )

        mock_write_dynamic_frame_from_options.assert_called_once_with(
            frame=sentinel.dynamic_frame,
            connection_type="s3",
            connection_options={"path": "s3://bucket/key/output-path"},
            format=format_name,
            format_options=format_options or {},
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame
