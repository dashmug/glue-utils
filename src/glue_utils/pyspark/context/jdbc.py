from __future__ import annotations  # noqa: D100

from typing import TYPE_CHECKING

from glue_utils.pyspark.connection_types import ConnectionType

if TYPE_CHECKING:
    from awsglue.context import GlueContext
    from awsglue.dynamicframe import DynamicFrame

    from glue_utils.pyspark.connection_options import (
        JDBCConnectionOptions,
        RedshiftJDBCConnectionOptions,
    )


class SQLServerMixin:
    """Mixin for working with SQL Server connections."""

    def create_dynamic_frame_from_sqlserver(
        self: GlueContext,
        connection_options: JDBCConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from a SQL Server database connection.

        Parameters
        ----------
        connection_options : JDBCConnectionOptions
            The connection options for the SQL Server database.
        transformation_ctx : str, optional
            The name of the transformation context. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame created from the SQL Server database.

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.SQLSERVER.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )

    def write_dynamic_frame_to_sqlserver(
        self: GlueContext,
        frame: DynamicFrame,
        connection_options: JDBCConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to a SQL Server database using JDBC.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to write to the SQL Server database.
        connection_options : JDBCConnectionOptions
            The JDBC connection options for the SQL Server database.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame that was written to the SQL Server database.

        """
        return self.write_dynamic_frame_from_options(
            frame=frame,
            connection_type=ConnectionType.SQLSERVER.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )


class MySQLMixin:
    """Mixin for working with MySQL connections."""

    def create_dynamic_frame_from_mysql(
        self: GlueContext,
        connection_options: JDBCConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from a MySQL database connection.

        Parameters
        ----------
        connection_options : JDBCConnectionOptions
            The connection options for the MySQL database.
        transformation_ctx : str, optional
            The transformation context for the DynamicFrame. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame created from the MySQL database.

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.MYSQL.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )

    def write_dynamic_frame_to_mysql(
        self: GlueContext,
        frame: DynamicFrame,
        connection_options: JDBCConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to a MySQL database using JDBC.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to write to the MySQL database.
        connection_options : JDBCConnectionOptions
            The JDBC connection options for the MySQL database.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame after writing to the MySQL database.

        """
        return self.write_dynamic_frame_from_options(
            frame=frame,
            connection_type=ConnectionType.MYSQL.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )


class OracleMixin:
    """Mixin for working with Oracle connections."""

    def create_dynamic_frame_from_oracle(
        self: GlueContext,
        connection_options: JDBCConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from an Oracle database connection.

        Parameters
        ----------
        connection_options : JDBCConnectionOptions
            The connection options for connecting to the Oracle database.
        transformation_ctx : str, optional
            The name of the transformation context. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame created from the Oracle database.

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.ORACLE.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )

    def write_dynamic_frame_to_oracle(
        self: GlueContext,
        frame: DynamicFrame,
        connection_options: JDBCConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to an Oracle database using JDBC.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to write to the Oracle database.
        connection_options : JDBCConnectionOptions
            The JDBC connection options for connecting to the Oracle database.
        transformation_ctx : str, optional
            The transformation context for the write operation. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame that was written to the Oracle database.

        """
        return self.write_dynamic_frame_from_options(
            frame=frame,
            connection_type=ConnectionType.ORACLE.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )


class PostgreSQLMixin:
    """Mixin for working with PostgreSQL connections."""

    def create_dynamic_frame_from_postgresql(
        self: GlueContext,
        connection_options: JDBCConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from a PostgreSQL database connection.

        Parameters
        ----------
        connection_options : JDBCConnectionOptions
            The connection options for the PostgreSQL database.
        transformation_ctx : str, optional
            The transformation context for the DynamicFrame. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame created from the PostgreSQL database.

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.POSTGRESQL.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )

    def write_dynamic_frame_to_postgresql(
        self: GlueContext,
        frame: DynamicFrame,
        connection_options: JDBCConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to a PostgreSQL database.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to write to the database.
        connection_options : JDBCConnectionOptions
            The JDBC connection options for the database.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame that was written to the database.

        """
        return self.write_dynamic_frame_from_options(
            frame=frame,
            connection_type=ConnectionType.POSTGRESQL.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )


class RedshiftSQLMixin:
    """Mixin for working with Redshift connections."""

    def create_dynamic_frame_from_redshift(
        self: GlueContext,
        connection_options: RedshiftJDBCConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from a Redshift database connection.

        Parameters
        ----------
        connection_options : RedshiftJDBCConnectionOptions
            The connection options for the Redshift database.
        transformation_ctx : str, optional
            The transformation context for the DynamicFrame. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame created from the Redshift database.

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.REDSHIFT.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )

    def write_dynamic_frame_to_redshift(
        self: GlueContext,
        frame: DynamicFrame,
        connection_options: RedshiftJDBCConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to a Redshift database.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to write to the database.
        connection_options : RedshiftJDBCConnectionOptions
            The JDBC connection options for the database.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame that was written to the database.

        """
        return self.write_dynamic_frame_from_options(
            frame=frame,
            connection_type=ConnectionType.REDSHIFT.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )


class JDBCMixin(
    MySQLMixin,
    OracleMixin,
    PostgreSQLMixin,
    RedshiftSQLMixin,
    SQLServerMixin,
):
    """Mixin for working with JDBC connections."""
