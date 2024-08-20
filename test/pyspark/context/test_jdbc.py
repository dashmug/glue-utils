from unittest.mock import sentinel

import pytest

from glue_utils.pyspark import (
    ConnectionType,
    GluePySparkContext,
)
from glue_utils.pyspark.connection_options import (
    JDBCConnectionOptions,
    RedshiftJDBCConnectionOptions,
)

CONNECTION_TYPES = [
    ConnectionType.MYSQL.value,
    ConnectionType.ORACLE.value,
    ConnectionType.POSTGRESQL.value,
    ConnectionType.SQLSERVER.value,
]


@pytest.mark.parametrize("connection_type", CONNECTION_TYPES)
class TestGluePySparkContextForJDBC:
    def test_create_dynamic_frame(
        self,
        connection_type: str,
        glue_pyspark_context: GluePySparkContext,
        mock_create_dynamic_frame_from_options,
    ) -> None:
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
    ) -> None:
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


class TestGluePySparkContextForJDBCRedshift:
    def test_create_dynamic_frame(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_create_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.create_dynamic_frame_from_redshift(
            connection_options=RedshiftJDBCConnectionOptions(
                url="something",
                user="user",
                dbtable="dbtable",
                password="password",  # noqa: S106
                redshiftTmpDir="temp-s3-dir",
                aws_iam_role="arn:aws:iam::account id:role/rs-role-name",
            ),
            transformation_ctx="test",
        )

        mock_create_dynamic_frame_from_options.assert_called_once_with(
            connection_type=ConnectionType.REDSHIFT.value,
            connection_options={
                "url": "something",
                "user": "user",
                "dbtable": "dbtable",
                "password": "password",
                "redshiftTmpDir": "temp-s3-dir",
                "aws_iam_role": "arn:aws:iam::account id:role/rs-role-name",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    def test_write_dynamic_frame(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_write_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.write_dynamic_frame_to_redshift(
            frame=sentinel.dynamic_frame,
            connection_options=RedshiftJDBCConnectionOptions(
                url="something",
                user="user",
                dbtable="dbtable",
                password="password",  # noqa: S106
                redshiftTmpDir="temp-s3-dir",
                aws_iam_role="arn:aws:iam::account id:role/rs-role-name",
            ),
            transformation_ctx="test",
        )

        mock_write_dynamic_frame_from_options.assert_called_once_with(
            frame=sentinel.dynamic_frame,
            connection_type=ConnectionType.REDSHIFT.value,
            connection_options={
                "url": "something",
                "user": "user",
                "dbtable": "dbtable",
                "password": "password",
                "redshiftTmpDir": "temp-s3-dir",
                "aws_iam_role": "arn:aws:iam::account id:role/rs-role-name",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame
