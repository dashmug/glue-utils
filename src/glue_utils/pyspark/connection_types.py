"""Module containing types for handling different connection types."""

from enum import Enum


class ConnectionType(Enum):
    """Enum class representing different types of connections."""

    DYNAMODB = "dynamodb"
    KINESIS = "kinesis"
    S3 = "s3"
    DOCUMENTDB = "documentdb"
    OPENSEARCH = "opensearch"
    REDSHIFT = "redshift"
    KAFKA = "kafka"
    AZURE_COSMOS = "azurecosmos"
    AZURE_SQL = "azuresql"
    BIGQUERY = "bigquery"
    MONGODB = "mongodb"
    SQLSERVER = "sqlserver"
    MYSQL = "mysql"
    ORACLE = "oracle"
    POSTGRESQL = "postgresql"
    SAPHANA = "saphana"
    SNOWFLAKE = "snowflake"
    TERADATA = "teradata"
    VERTICA = "vertica"
    MARKETPLACE_ATHENA = "marketplace.athena"
    MARKETPLACE_SPARK = "marketplace.spark"
    MARKETPLACE_JDBC = "marketplace.jdbc"
    CUSTOM_ATHENA = "custom.athena"
    CUSTOM_SPARK = "custom.spark"
    CUSTOM_JDBC = "custom.jdbc"
