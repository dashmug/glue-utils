from enum import Enum  # noqa: D100


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
