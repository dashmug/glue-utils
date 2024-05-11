from __future__ import annotations  # noqa: D100

from enum import Enum
from typing import TYPE_CHECKING, Literal, TypedDict

from .connection_types import ConnectionType

if TYPE_CHECKING:
    from awsglue.context import GlueContext
    from awsglue.dynamicframe import DynamicFrame


class Format(Enum):
    """Enum representing different file formats."""

    AVRO = "avro"
    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    ORC = "orc"
    XML = "xml"
    GROKLOG = "grokLog"
    ION = "ion"


class S3SourceConnectionOptions(TypedDict, total=False):
    """Connection options for S3 connections.

    References
    ----------
    - AWS Glue Programming ETL Connect to S3:
      https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-s3-home.html

    """

    paths: list[str]
    exclusions: str
    compressionType: Literal["gzip", "bzip2"]
    groupFiles: Literal["inPartition", "none"]
    groupSize: str
    recurse: bool
    maxBand: int
    maxFilesInBand: int
    isFailFast: bool
    catalogPartitionPredicate: str
    excludeStorageClasses: list[str]


class S3SinkConnectionOptions(TypedDict, total=False):
    """Connection options for writing data to an S3 sink."""

    path: str
    compression: Literal["gzip", "bzip2"]
    partitionKeys: list[str]


class S3FormatOptions(TypedDict, total=False):
    """Common format options for S3."""

    attachFilename: str
    attachTimestamp: str


class CSVFormatOptions(S3FormatOptions, total=False):
    """Format options for CSV files.

    Reference
    ---------
    - AWS Glue Programming ETL Connect to CSV:
      https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-csv-home.html

    """

    separator: str
    escaper: str
    quoteChar: str
    multiLine: bool
    withHeader: bool
    writeHeader: bool
    skipFirst: bool
    optimizePerformance: bool
    strictCheckForQuoting: bool


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
        connection_options: S3SourceConnectionOptions,
        format_options: CSVFormatOptions | None = None,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to a CSV file in Amazon S3.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to write.
        connection_options : S3SourceConnectionOptions
            The connection options for the S3 source.
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


class ParquetFormatOptions(S3FormatOptions, total=False):
    """Format options for Parquet files.

    Reference
    ---------
    - AWS Glue Programming ETL Connect to Parquet:
      https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-parquet-home.html

    """

    useGlueParquetWriter: bool
    compression: Literal[
        "uncompressed",
        "snappy",
        "gzip",
        "lzo",
    ]
    blockSize: int
    pageSize: int


class S3ParquetMixin:
    """Mixin for working with Parquet files in S3."""

    def create_dynamic_frame_from_s3_parquet(
        self: GlueContext,
        connection_options: S3SourceConnectionOptions,
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


class JSONFormatOptions(S3FormatOptions, total=False):
    """Format options for JSON files.

    Reference
    ---------
    - AWS Glue Programming ETL Connect to JSON:
      https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-json-home.html

    """

    jsonPath: str
    multiline: bool
    optimizePerformance: bool
    withSchema: str


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


class XMLFormatOptions(S3FormatOptions, total=False):
    """Format options for XML files.

    Reference
    ---------
    - AWS Glue Programming ETL Connect to XML:
      https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-xml-home.html#aws-glue-programming-etl-format-xml-reference

    """

    rowTag: str
    encoding: str
    excludeAttribute: bool
    treatEmptyValueAsNull: bool
    attributePrefix: str
    valueTag: str
    ignoreSurroundingSpaces: bool
    withSchema: str


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
