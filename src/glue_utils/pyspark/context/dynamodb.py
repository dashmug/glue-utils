from __future__ import annotations  # noqa: D100

from typing import TYPE_CHECKING

from glue_utils.pyspark.connection_types import ConnectionType

if TYPE_CHECKING:
    from awsglue.context import GlueContext
    from awsglue.dynamicframe import DynamicFrame

    from glue_utils.pyspark.connection_options import (
        DynamoDBExportSourceConnectionOptions,
        DynamoDBSinkConnectionOptions,
        DynamoDBSourceConnectionOptions,
    )


class DynamoDBMixin:
    """Mixin for working with DynamoDB connections."""

    def create_dynamic_frame_from_dynamodb(
        self: GlueContext,
        connection_options: DynamoDBSourceConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from a DynamoDB data source.

        This uses the AWS Glue DynamoDB ETL connector.

        Parameters
        ----------
        connection_options : DynamoDBSourceConnectionOptions
            The connection options for the DynamoDB data source.
        transformation_ctx : str, optional
            The transformation context for the dynamic frame. Defaults to "".

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.DYNAMODB.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )

    def create_dynamic_frame_from_dynamodb_export(
        self: GlueContext,
        connection_options: DynamoDBExportSourceConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from a DynamoDB data source.

        This uses the AWS Glue DynamoDB Export connector.

        Parameters
        ----------
        connection_options : DynamoDBSourceConnectionOptions
            The connection options for the DynamoDB data source.
        transformation_ctx : str, optional
            The transformation context for the dynamic frame. Defaults to "".

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.DYNAMODB.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )

    def write_dynamic_frame_to_dynamodb(
        self: GlueContext,
        frame: DynamicFrame,
        connection_options: DynamoDBSinkConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to DynamoDB using the specified connection options.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to write to DynamoDB.
        connection_options : DynamoDBSinkConnectionOptions
            The connection options for DynamoDB.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        """
        return self.write_dynamic_frame_from_options(
            frame=frame,
            connection_type=ConnectionType.DYNAMODB.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )
