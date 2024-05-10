from unittest.mock import patch, sentinel

import pytest
from glue_utils.pyspark import (
    CSVFormatOptions,
    GluePySparkContext,
    JDBCConnectionOptions,
    JSONFormatOptions,
    ParquetFormatOptions,
    S3FormatOptions,
    S3SinkConnectionOptions,
    S3SourceConnectionOptions,
    XMLFormatOptions,
)
from pyspark import SparkContext


@pytest.fixture(scope="session")
def glue_pyspark_context():
    sc = SparkContext.getOrCreate()
    yield GluePySparkContext(sc)
    sc.stop()


@pytest.fixture
def mock_create_dynamic_frame_from_options(glue_pyspark_context):
    with patch.object(
        glue_pyspark_context,
        "create_dynamic_frame_from_options",
        wraps=glue_pyspark_context.create_dynamic_frame_from_options,
        return_value=sentinel.dynamic_frame,
    ) as patched:
        yield patched


@pytest.fixture
def mock_write_dynamic_frame_from_options(glue_pyspark_context):
    with patch.object(
        glue_pyspark_context,
        "write_dynamic_frame_from_options",
        wraps=glue_pyspark_context.write_dynamic_frame_from_options,
        return_value=sentinel.dynamic_frame,
    ) as patched:
        yield patched


CONNECTION_TYPES = ["sqlserver", "mysql", "postgresql", "oracle"]


@pytest.mark.parametrize("connection_type", CONNECTION_TYPES)
class TestGluePySparkContextForJDBC:
    def test_create_dynamic_frame(
        self,
        connection_type: str,
        glue_pyspark_context: GluePySparkContext,
        mock_create_dynamic_frame_from_options,
    ):
        create_dynamic_frame = getattr(
            glue_pyspark_context,
            f"create_dynamic_frame_from_{connection_type}",
        )
        dynamic_frame = create_dynamic_frame(
            connection_options=JDBCConnectionOptions(
                url="something",
                user="user",
                dbtable="dbtable",
                password="password",  # noqa: S106
            ),
            transformation_ctx="test",
        )

        mock_create_dynamic_frame_from_options.assert_called_once_with(
            connection_type=connection_type,
            connection_options={
                "url": "something",
                "user": "user",
                "dbtable": "dbtable",
                "password": "password",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    def test_write_dynamic_frame(
        self,
        connection_type: str,
        glue_pyspark_context: GluePySparkContext,
        mock_write_dynamic_frame_from_options,
    ):
        write_dynamic_frame = getattr(
            glue_pyspark_context,
            f"write_dynamic_frame_to_{connection_type}",
        )
        dynamic_frame = write_dynamic_frame(
            frame=sentinel.dynamic_frame,
            connection_options=JDBCConnectionOptions(
                url="something",
                user="user",
                dbtable="dbtable",
                password="password",  # noqa: S106
            ),
            transformation_ctx="test",
        )

        mock_write_dynamic_frame_from_options.assert_called_once_with(
            frame=sentinel.dynamic_frame,
            connection_type=connection_type,
            connection_options={
                "url": "something",
                "user": "user",
                "dbtable": "dbtable",
                "password": "password",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame


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
            format_options=format_options_cls(**format_options),
            transformation_ctx="test",
        )

        mock_create_dynamic_frame_from_options.assert_called_once_with(
            connection_type="s3",
            connection_options={"paths": ["s3://bucket/key/input-path"]},
            format=format_name,
            format_options=format_options,
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
            else None,
            transformation_ctx="test",
        )

        mock_write_dynamic_frame_from_options.assert_called_once_with(
            frame=sentinel.dynamic_frame,
            connection_type="s3",
            connection_options={"path": "s3://bucket/key/output-path"},
            format=format_name,
            format_options=format_options,
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame
