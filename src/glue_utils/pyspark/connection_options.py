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
    bulkSize: int
    hashfield: str
    hashexpression: str
    hashpartitions: int
    sampleQuery: str
    enablePartitioningForSampleQuery: bool
    sampleSize: int


# Redshift has a connection option with a dot in it, so we need to use
# this form of TypedDict to define the connection options.
RedshiftOptions = TypedDict(
    "RedshiftOptions",
    {
        "autopushdown": bool,
        "autopushdown.s3_result_cache": bool,
        "aws_iam_role": str,
        "csvnullstring": str,
        "DbUser": str,
        "extracopyoptions": str,
        "redshiftTmpDir": str,
        "sse_kms_key": str,
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
    maxBand: int
    maxFilesInBand: int
    isFailFast: bool
    catalogPartitionPredicate: str
    excludeStorageClasses: list[str]
    useS3ListImplementation: bool


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
        "dynamodb.throughput.read.percent": float,
        "dynamodb.splits": int,
        "dynamodb.sts.roleArn": str,
        "dynamodb.sts.roleSessionName": str,
        "dynamodb.sts.region": str,
        "dynamodb.export": Literal["ddb", "s3"],
        "dynamodb.tableArn": str,
        "dynamodb.s3.bucket": str,
        "dynamodb.s3.prefix": str,
        "dynamodb.s3.bucketOwner": str,
        "dynamodb.simplifyDDBJson": bool,
        "dynamodb.exportTime": str,
    },
    total=False,
)

# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-dynamodb-home.html
DynamoDBSinkConnectionOptions = TypedDict(
    "DynamoDBSinkConnectionOptions",
    {
        "dynamodb.output.tableName": str,
        "dynamodb.throughput.write.percent": float,
        "dynamodb.output.numParallelTasks": int,
        "dynamodb.output.retry": int,
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
    failOnDataLoss: bool
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
    maxFetchTimeInMs: int
    maxFetchRecordsPerShard: int
    maxRecordPerRead: int
    addIdleTimeBetweenReads: bool
    idleTimeBetweenReadsInMs: int
    describeShardInterval: str
    numRetries: int
    retryIntervalMs: int
    maxRetryIntervalMs: int
    avoidEmptyBatches: bool
    schema: str
    inferSchema: bool
    addRecordTimestamp: bool
    emitConsumerLagMetrics: bool
    fanoutConsumerARN: str


class KinesisSinkConnectionOptions(KinesisConnectionOptions, total=False):
    """Connection options for writing to Kinesis."""

    partitionKey: str
    recordMaxBufferedTime: int
    aggregationEnabled: bool
    aggregationMaxSize: int
    aggregationMaxCount: int
    producerRateLimit: int
    collectionMaxCount: int
    collectionMaxSize: int


# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-documentdb-home.html
DocumentDBSourceConnectionOptions = TypedDict(
    "DocumentDBSourceConnectionOptions",
    {
        "uri": str,
        "database": str,
        "collection": str,
        "username": str,
        "password": str,
        "ssl": bool,
        "ssl.domain_match": bool,
        "batchSize": int,
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
    extendedBSONTypes: bool
    replaceDocument: bool
    maxBatchSize: int
    retryWrites: bool


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
        "ssl": bool,
        "ssl.domain_match": bool,
        "disableUpdateUri": bool,
        "batchSize": int,
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
        "ssl": bool,
        "ssl.domain_match": bool,
        "disableUpdateUri": bool,
        "extendedBSONTypes": bool,
        "replaceDocument": bool,
        "maxBatchSize": int,
        "retryWrites": bool,
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
        "pushdown": bool,
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
        "security.protocol": str,
        "topicName": str,
        "assign": str,
        "subscribePattern": str,
        "classification": str,
        "delimiter": str,
        "startingOffsets": str,
        "startingTimestamp": str,
        "endingOffsets": str,
        "pollTimeoutMs": int,
        "numRetries": int,
        "retryIntervalMs": int,
        "maxOffsetsPerTrigger": int,
        "minPartitions": int,
        "includeHeaders": bool,
        "schema": str,
        "inferSchema": bool,
        "addRecordTimestamp": bool,
        "emitConsumerLagMetrics": bool,
    },
    total=False,
)


class KafkaSinkConnectionOptions(TypedDict, total=False):
    """Connection options for writing to Kafka.

    Reference:
    - https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect-kafka-home.html
    """

    connectionName: str
    topic: str
    partition: str
    key: str
    classification: str
