"""Module containing GluePySparkContext class that extends GlueContext."""

from __future__ import annotations

from awsglue.context import GlueContext

from .mixins.jdbc import JDBCMixin
from .mixins.s3 import S3Mixin


class GluePySparkContext(
    JDBCMixin,
    S3Mixin,
    # error: Class cannot subclass "AWSGlueContext" (has type "Any")  [misc]
    GlueContext,  # type: ignore[misc]
):
    """A custom PySpark context that extends the functionality of the AWS GlueContext.

    This class combines the features of the mixin classes with the AWS
    GlueContext to provide additional functionality for working with
    JDBC and S3 data sources in a Glue job.
    """
