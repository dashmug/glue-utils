"""Module containing GluePySparkContext class that extends GlueContext."""

from __future__ import annotations

from typing import TypedDict

from awsglue.context import GlueContext

from .documentdb import DocumentDBMixin
from .dynamodb import DynamoDBMixin
from .jdbc import JDBCMixin
from .kafka import KafkaMixin
from .kinesis import KinesisMixin
from .mongodb import MongoDBMixin
from .opensearch import OpenSearchMixin
from .s3 import S3Mixin


class GlueContextOptions(TypedDict, total=False):
    """Options to be passed as kwargs when instantiating a GlueContext object."""

    minPartitions: int
    targetPartitions: int


class GluePySparkContext(
    DocumentDBMixin,
    DynamoDBMixin,
    JDBCMixin,
    KafkaMixin,
    KinesisMixin,
    MongoDBMixin,
    OpenSearchMixin,
    S3Mixin,
    # awsglue has no typings yet
    GlueContext,  # type: ignore[misc]
):
    """A custom PySpark context that extends the functionality of the AWS GlueContext.

    This class combines the features of the mixin classes with the AWS
    GlueContext to provide additional functionality for working with
    JDBC and S3 data sources in a Glue job.
    """
