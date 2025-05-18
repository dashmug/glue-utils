"""Module containing dictionary structures for handling different connection types."""

from typing import Literal, TypedDict


class BookmarkConnectionOptions(TypedDict, total=False):
    """TypedDict class representing general connection options.

    Reference
    ---------
    - https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect.html#aws-glue-programming-etl-connect-general-options

    """

    jobBookmarkKeys: list[str]
    jobBookmarkKeysSortOrder: Literal["asc", "desc"]


class JDBCConnectionOptions(BookmarkConnectionOptions, total=False):
    """Connection options for JDBC connections.

    Reference
    ---------
    - https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-jdbc-home.html

    """

    useConnectionProperties: Literal["true"]
    connectionName: str
    databaseName: str
    url: str
    dbtable: str
    user: str
    password: str
    customJdbcDriverS3Path: str
    customJdbcDriverClassName: str
    bulkSize: str
    hashfield: str
    hashexpression: str
    hashpartitions: str
    sampleQuery: str
    enablePartitioningForSampleQuery: Literal["true", "false"]
    sampleSize: str


# Redshift has a connection option with a dot in it, so we need to use
# this form of TypedDict to define the connection options.
# https://docs.aws.amazon.com/redshift/latest/mgmt/spark-redshift-connector-other-config.html
RedshiftOptions = TypedDict(
    "RedshiftOptions",
    {
        "autopushdown.s3_result_cache": Literal["true", "false"],
        "autopushdown": Literal["true", "false"],
        "aws_iam_role": str,
        "copydelay": int,
        "copyretrytimeout": int,
        "csvnullstring": str,
        "DbUser": str,
        "description": str,
        "distkey": str,
        "diststyle": Literal["AUTO", "EVEN", "KEY", "ALL"],
        "extracopyoptions": str,
        "extraunloadoptions": str,
        "forward_spark_s3_credentials": bool,
        "include_column_list": bool,
        "jdbcdriver": str,
        "label": str,
        "postcopyoptions": str,
        "preactions": str,
        "query": str,
        "redshiftTmpDir": str,
        "secret.id": str,
        "secret.region": str,
        "secret.vpcEndpointRegion": str,
        "secret.vpcEndpointUrl": str,
        "sortkeyspec": str,
        "sse_kms_key": str,
        "tempdir_region": str,
        "tempdir": str,
        "tempformat": Literal["AVRO", "CSV", "CSV GZIP"],
        "temporary_aws_access_key_id": str,
        "temporary_aws_secret_access_key": str,
        "temporary_aws_session_token": str,
        "unload_s3_format": Literal["TEXT", "PARQUET"],
    },
    total=False,
)


class RedshiftJDBCConnectionOptions(
    RedshiftOptions, JDBCConnectionOptions, total=False
):
    """Connection options for Redshift JDBC connections.

    Reference
    ---------
    - https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-redshift-home.html

    """


class S3SourceConnectionOptions(BookmarkConnectionOptions, total=False):
    """Connection options for S3 connections.

    Reference
    ---------
    - AWS Glue Programming ETL Connect to S3:
      https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-s3-home.html

    """

    paths: list[str]
    exclusions: str
    compressionType: Literal["gzip", "bzip2"]
    groupFiles: Literal["inPartition", "none"]
    groupSize: str
    recurse: bool
    maxBand: str
    maxFilesInBand: str
    isFailFast: bool
    catalogPartitionPredicate: str
    excludeStorageClasses: list[str]
    useS3ListImplementation: bool


class S3ParquetSourceConnectionOptions(S3SourceConnectionOptions, total=False):
    """Additional connection options when using Parquet files in S3.

    Reference
    ---------
    - Using the Parquet format in AWS Glue:
      https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-parquet-home.html

    """

    mergeSchema: bool


class S3SinkConnectionOptions(BookmarkConnectionOptions, total=False):
    """Connection options for writing data to an S3 sink."""

    path: str
    compression: Literal["gzip", "bzip2"]
    partitionKeys: list[str]


# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-dynamodb-home.html
DynamoDBSourceConnectionOptions = TypedDict(
    "DynamoDBSourceConnectionOptions",
    {
        "dynamodb.input.tableName": str,
        "dynamodb.throughput.read.percent": str,
        "dynamodb.splits": str,
        "dynamodb.sts.roleArn": str,
        "dynamodb.sts.roleSessionName": str,
    },
    total=False,
)

# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-dynamodb-home.html
DynamoDBExportSourceConnectionOptions = TypedDict(
    "DynamoDBExportSourceConnectionOptions",
    {
        "dynamodb.export": Literal["ddb", "s3"],
        "dynamodb.tableArn": str,
        "dynamodb.s3.bucket": str,
        "dynamodb.s3.prefix": str,
        "dynamodb.s3.bucketOwner": str,
        "dynamodb.simplifyDDBJson": Literal["true", "false"],
        "dynamodb.exportTime": str,
        "dynamodb.sts.region": str,
    },
    total=False,
)

# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-dynamodb-home.html
DynamoDBSinkConnectionOptions = TypedDict(
    "DynamoDBSinkConnectionOptions",
    {
        "dynamodb.output.tableName": str,
        "dynamodb.throughput.write.percent": str,
        "dynamodb.output.numParallelTasks": str,
        "dynamodb.output.retry": str,
        "dynamodb.sts.roleArn": str,
        "dynamodb.sts.roleSessionName": str,
    },
    total=False,
)


class KinesisConnectionOptions(TypedDict, total=False):
    """Connection options for Kinesis connections.

    Reference
    ---------
    - https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-kinesis-home.html

    """

    streamARN: str
    failOnDataLoss: Literal["true", "false"]
    awsSTSRoleArn: str
    awsSTSSessionName: str
    awsSTSEndpoint: str


class KinesisSourceConnectionOptions(KinesisConnectionOptions, total=False):
    """Connection options to read from Kinesis."""

    classification: str
    streamName: str
    endpointUrl: str
    delimiter: str
    startingPosition: str
    maxFetchTimeInMs: str
    maxFetchRecordsPerShard: str
    maxRecordPerRead: str
    addIdleTimeBetweenReads: Literal["true", "false"]
    idleTimeBetweenReadsInMs: str
    describeShardInterval: str
    numRetries: str
    retryIntervalMs: str
    maxRetryIntervalMs: str
    avoidEmptyBatches: Literal["true", "false"]
    schema: str
    inferSchema: Literal["true", "false"]
    addRecordTimestamp: Literal["true", "false"]
    emitConsumerLagMetrics: Literal["true", "false"]
    fanoutConsumerARN: str


class KinesisSinkConnectionOptions(KinesisConnectionOptions, total=False):
    """Connection options for writing to Kinesis."""

    partitionKey: str
    recordMaxBufferedTime: str
    aggregationEnabled: Literal["true", "false"]
    aggregationMaxSize: str
    aggregationMaxCount: str
    producerRateLimit: str
    collectionMaxCount: str
    collectionMaxSize: str


# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-documentdb-home.html
DocumentDBSourceConnectionOptions = TypedDict(
    "DocumentDBSourceConnectionOptions",
    {
        "uri": str,
        "database": str,
        "collection": str,
        "username": str,
        "password": str,
        "ssl": str,
        "ssl.domain_match": str,
        "batchSize": str,
        "partitioner": str,
        "partitionerOptions.partitionKey": str,
        "partitionerOptions.partitionSizeMB": str,
        "partitionerOptions.samplesPerPartition": str,
        "partitionerOptions.shardKey": str,
        "partitionerOptions.numberOfPartitions": str,
    },
    total=False,
)


class DocumentDBSinkConnectionOptions(TypedDict, total=False):
    """Connection options for writing to DocumentDB.

    Reference:
    - https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-documentdb-home.html
    """

    uri: str
    database: str
    collection: str
    username: str
    password: str
    extendedBSONTypes: str
    replaceDocument: str
    maxBatchSize: str
    retryWrites: str


# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-mongodb-home.html
MongoDBSourceConnectionOptions = TypedDict(
    "MongoDBSourceConnectionOptions",
    {
        "connectionName": str,
        "uri": str,
        "connection.uri": str,
        "username": str,
        "password": str,
        "database": str,
        "collection": str,
        "ssl": Literal["true", "false"],
        "ssl.domain_match": Literal["true", "false"],
        "disableUpdateUri": Literal["true", "false"],
        "batchSize": str,
        "partitioner": str,
        "partitionerOptions.partitionKey": str,
        "partitionerOptions.partitionSizeMB": str,
        "partitionerOptions.samplesPerPartition": str,
        "partitionerOptions.shardKey": str,
        "partitionerOptions.numberOfPartitions": str,
    },
    total=False,
)

# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-mongodb-home.html
MongoDBSinkConnectionOptions = TypedDict(
    "MongoDBSinkConnectionOptions",
    {
        "connectionName": str,
        "uri": str,
        "connection.uri": str,
        "username": str,
        "password": str,
        "database": str,
        "collection": str,
        "ssl": Literal["true", "false"],
        "ssl.domain_match": Literal["true", "false"],
        "disableUpdateUri": Literal["true", "false"],
        "extendedBSONTypes": Literal["true", "false"],
        "replaceDocument": Literal["true", "false"],
        "maxBatchSize": str,
        "retryWrites": Literal["true", "false"],
    },
    total=False,
)

# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-opensearch-home.html
OpenSearchSourceConnectionOptions = TypedDict(
    "OpenSearchSourceConnectionOptions",
    {
        "connectionName": str,
        "opensearch.resource": str,
        "opensearch.query": str,
        "pushdown": Literal["true", "false"],
        "opensearch.read.field.as.array.include": str,
    },
    total=False,
)

# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-opensearch-home.html
OpenSearchSinkConnectionOptions = TypedDict(
    "OpenSearchSinkConnectionOptions",
    {
        "connectionName": str,
        "opensearch.resource": str,
    },
    total=False,
)

# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-kafka-home.html
KafkaSourceConnectionOptions = TypedDict(
    "KafkaSourceConnectionOptions",
    {
        "connectionName": str,
        "bootstrap.servers": str,
        "security.protocol": Literal["SSL", "PLAINTEXT"],
        "topicName": str,
        "assign": str,
        "subscribePattern": str,
        "classification": str,
        "delimiter": str,
        "startingOffsets": Literal["earliest", "latest"],
        "startingTimestamp": str,
        "endingOffsets": str,
        "pollTimeoutMs": str,
        "numRetries": str,
        "retryIntervalMs": str,
        "maxOffsetsPerTrigger": str,
        "minPartitions": str,
        "includeHeaders": Literal["true", "false"],
        "schema": str,
        "inferSchema": Literal["true", "false"],
        "addRecordTimestamp": Literal["true", "false"],
        "emitConsumerLagMetrics": Literal["true", "false"],
    },
    total=False,
)


class KafkaSinkConnectionOptions(TypedDict, total=False):
    """Connection options for writing to Kafka.

    Reference:
    - https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-kafka-home.html
    """

    connectionName: str
    topicName: str
    partition: str
    key: str
    classification: str
