from importlib.util import find_spec

if not find_spec("awsglue.context"):
    msg = (
        "GlueContext is required to use this module. "
        "Make sure you are running within a Glue PySpark environment."
    )
    raise ModuleNotFoundError(msg)

from .connection_options import (
    DocumentDBSinkConnectionOptions,
    DocumentDBSourceConnectionOptions,
    DynamoDBExportSourceConnectionOptions,
    DynamoDBSinkConnectionOptions,
    DynamoDBSourceConnectionOptions,
    JDBCConnectionOptions,
    KafkaSinkConnectionOptions,
    KafkaSourceConnectionOptions,
    KinesisSinkConnectionOptions,
    KinesisSourceConnectionOptions,
    MongoDBSinkConnectionOptions,
    MongoDBSourceConnectionOptions,
    OpenSearchSinkConnectionOptions,
    OpenSearchSourceConnectionOptions,
    RedshiftJDBCConnectionOptions,
    S3ParquetSourceConnectionOptions,
    S3SinkConnectionOptions,
    S3SourceConnectionOptions,
)
from .connection_types import ConnectionType
from .context import GluePySparkContext
from .format_options import (
    CSVFormatOptions,
    JSONFormatOptions,
    ParquetFormatOptions,
    S3FormatOptions,
    XMLFormatOptions,
)
from .formats import Format
from .job import GluePySparkJob

__all__ = [
    "ConnectionType",
    "CSVFormatOptions",
    "DocumentDBSinkConnectionOptions",
    "DocumentDBSourceConnectionOptions",
    "DynamoDBSinkConnectionOptions",
    "DynamoDBSourceConnectionOptions",
    "DynamoDBExportSourceConnectionOptions",
    "Format",
    "GluePySparkContext",
    "GluePySparkJob",
    "JDBCConnectionOptions",
    "JSONFormatOptions",
    "KafkaSinkConnectionOptions",
    "KafkaSourceConnectionOptions",
    "KinesisSinkConnectionOptions",
    "KinesisSourceConnectionOptions",
    "MongoDBSinkConnectionOptions",
    "MongoDBSourceConnectionOptions",
    "OpenSearchSinkConnectionOptions",
    "OpenSearchSourceConnectionOptions",
    "ParquetFormatOptions",
    "RedshiftJDBCConnectionOptions",
    "S3FormatOptions",
    "S3SinkConnectionOptions",
    "S3SourceConnectionOptions",
    "S3ParquetSourceConnectionOptions",
    "XMLFormatOptions",
]
