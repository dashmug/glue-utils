"""Module containing dictionary structures for handling different format options."""

from typing import Literal, TypedDict


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
