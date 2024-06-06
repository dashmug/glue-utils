from __future__ import annotations  # noqa: D100

from typing import TYPE_CHECKING

from glue_utils.pyspark.connection_types import ConnectionType
from glue_utils.pyspark.formats import Format

if TYPE_CHECKING:
    from awsglue.context import GlueContext
    from awsglue.dynamicframe import DynamicFrame

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


class S3CSVMixin:
    """Mixin for working with CSV files in S3."""

    def create_dynamic_frame_from_s3_csv(
        self: GlueContext,
        connection_options: S3SourceConnectionOptions,
        format_options: CSVFormatOptions | None = None,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from a CSV file stored in Amazon S3.

        Parameters
        ----------
        connection_options : S3SourceConnectionOptions
            The connection options for the S3 source.
        format_options : CSVFormatOptions | None, optional
            The format options for the CSV file. Defaults to None.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame created from the CSV file in S3.

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.S3.value,
            connection_options=connection_options,
            format=Format.CSV.value,
            format_options=format_options or {},
            transformation_ctx=transformation_ctx,
        )

    def write_dynamic_frame_to_s3_csv(
        self: GlueContext,
        frame: DynamicFrame,
        connection_options: S3SinkConnectionOptions,
        format_options: CSVFormatOptions | None = None,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to a CSV file in Amazon S3.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to write.
        connection_options : S3SinkConnectionOptions
            The connection options for the S3 sink.
        format_options : CSVFormatOptions | None, optional
            The format options for the CSV file. Defaults to None.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        Returns
        -------
        DynamicFrame
            The written DynamicFrame.

        """
        return self.write_dynamic_frame_from_options(
            frame=frame,
            connection_type=ConnectionType.S3.value,
            connection_options=connection_options,
            format=Format.CSV.value,
            format_options=format_options or {},
            transformation_ctx=transformation_ctx,
        )


class S3ParquetMixin:
    """Mixin for working with Parquet files in S3."""

    def create_dynamic_frame_from_s3_parquet(
        self: GlueContext,
        connection_options: S3ParquetSourceConnectionOptions,
        format_options: ParquetFormatOptions | None = None,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from Parquet files stored in Amazon S3.

        Parameters
        ----------
        connection_options : S3SourceConnectionOptions
            The connection options for the S3 source.
        format_options : ParquetFormatOptions | None, optional
            The format options for reading Parquet files. Defaults to None.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame created from the Parquet files in S3.

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.S3.value,
            connection_options=connection_options,
            format=Format.PARQUET.value,
            format_options=format_options or {},
            transformation_ctx=transformation_ctx,
        )

    def write_dynamic_frame_to_s3_parquet(
        self: GlueContext,
        frame: DynamicFrame,
        connection_options: S3SinkConnectionOptions,
        format_options: ParquetFormatOptions | None = None,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to Parquet format in Amazon S3.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to write.
        connection_options : S3SinkConnectionOptions
            The connection options for writing to S3.
        format_options : ParquetFormatOptions | None, optional
            The format options for writing Parquet. Defaults to None.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        Returns
        -------
        DynamicFrame
            The written DynamicFrame.

        """
        return self.write_dynamic_frame_from_options(
            frame=frame,
            connection_type=ConnectionType.S3.value,
            connection_options=connection_options,
            format=Format.PARQUET.value,
            format_options=format_options or {},
            transformation_ctx=transformation_ctx,
        )


class S3JSONMixin:
    """Mixin for working with JSON files in S3."""

    def create_dynamic_frame_from_s3_json(
        self: GlueContext,
        connection_options: S3SourceConnectionOptions,
        format_options: JSONFormatOptions | None = None,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from JSON data stored in Amazon S3.

        Parameters
        ----------
        connection_options : S3SourceConnectionOptions
            The connection options for the S3 source.
        format_options : JSONFormatOptions | None, optional
            The format options for the JSON data. Defaults to None.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame created from the JSON data in S3.

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.S3.value,
            connection_options=connection_options,
            format=Format.JSON.value,
            format_options=format_options or {},
            transformation_ctx=transformation_ctx,
        )

    def write_dynamic_frame_to_s3_json(
        self: GlueContext,
        frame: DynamicFrame,
        connection_options: S3SinkConnectionOptions,
        format_options: JSONFormatOptions | None = None,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to JSON format and save it in S3.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to be written.
        connection_options : S3SinkConnectionOptions
            The connection options for S3 sink.
        format_options : JSONFormatOptions | None, optional
            The format options for JSON. Defaults to None.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame after writing to S3.

        """
        return self.write_dynamic_frame_from_options(
            frame=frame,
            connection_type=ConnectionType.S3.value,
            connection_options=connection_options,
            format=Format.JSON.value,
            format_options=format_options or {},
            transformation_ctx=transformation_ctx,
        )


class S3XMLMixin:
    """Mixin for working with XML files in S3."""

    def create_dynamic_frame_from_s3_xml(
        self: GlueContext,
        connection_options: S3SourceConnectionOptions,
        format_options: XMLFormatOptions | None = None,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from XML data stored in Amazon S3.

        Parameters
        ----------
        connection_options : S3SourceConnectionOptions
            The connection options for the S3 data source.
        format_options : XMLFormatOptions, optional
            The format options for parsing the XML data. Defaults to None.
        transformation_ctx : str, optional
            The transformation context for the DynamicFrame. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame containing the parsed XML data.

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.S3.value,
            connection_options=connection_options,
            format=Format.XML.value,
            format_options=format_options or {},
            transformation_ctx=transformation_ctx,
        )

    def write_dynamic_frame_to_s3_xml(
        self: GlueContext,
        frame: DynamicFrame,
        connection_options: S3SinkConnectionOptions,
        format_options: XMLFormatOptions | None = None,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to XML format and saves it in S3.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to be written.
        connection_options : S3SinkConnectionOptions
            The connection options for S3 sink.
        format_options : XMLFormatOptions | None, optional
            The format options for XML. Defaults to None.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        Returns
        -------
        DynamicFrame
            The DynamicFrame after writing to S3.

        """
        return self.write_dynamic_frame_from_options(
            frame=frame,
            connection_type=ConnectionType.S3.value,
            connection_options=connection_options,
            format=Format.XML.value,
            format_options=format_options or {},
            transformation_ctx=transformation_ctx,
        )


class S3Mixin(S3CSVMixin, S3ParquetMixin, S3JSONMixin, S3XMLMixin):
    """Mixin for working with S3 connections."""
