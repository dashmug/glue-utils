"""Module containing dictionary structures for handling different format options."""

from __future__ import annotations

from typing import Literal, TypedDict


class S3FormatOptions(TypedDict, total=False):
    """Common format options for S3."""

    attachFilename: str
    attachTimestamp: str


class CSVFormatOptions(S3FormatOptions, total=False):
    """Format options for CSV files.

    Reference
    ---------
    - Using the CSV format in AWS Glue:
      https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-csv-home.html

    """

    separator: str
    escaper: str
    quoteChar: str | Literal[-1]
    multiLine: bool
    withHeader: bool
    writeHeader: bool
    skipFirst: bool
    optimizePerformance: bool
    strictCheckForQuoting: bool


class ParquetFormatOptions(S3FormatOptions, total=False):
    """Format options for Parquet files.

    Reference
    ---------
    - Using the Parquet format in AWS Glue:
      https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-parquet-home.html

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


class JSONFormatOptions(S3FormatOptions, total=False):
    """Format options for JSON files.

    Reference
    ---------
    - Using the JSON format in AWS Glue:
      https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-json-home.html

    """

    jsonPath: str
    multiline: bool
    optimizePerformance: bool
    withSchema: str


class XMLFormatOptions(S3FormatOptions, total=False):
    """Format options for XML files.

    Reference
    ---------
    - Using the XML format in AWS Glue:
      https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-xml-home.html

    """

    rowTag: str
    encoding: str
    excludeAttribute: bool
    treatEmptyValueAsNull: bool
    attributePrefix: str
    valueTag: str
    ignoreSurroundingSpaces: bool
    withSchema: str
