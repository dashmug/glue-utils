from __future__ import annotations  # noqa: D100

from typing import TYPE_CHECKING

from glue_utils.pyspark.connection_types import ConnectionType

if TYPE_CHECKING:
    from awsglue.context import GlueContext
    from awsglue.dynamicframe import DynamicFrame

    from glue_utils.pyspark.connection_options import (
        MongoDBSinkConnectionOptions,
        MongoDBSourceConnectionOptions,
    )


class MongoDBMixin:
    """Mixin for working with Mongodb connections."""

    def create_dynamic_frame_from_mongodb(
        self: GlueContext,
        connection_options: MongoDBSourceConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from a Mongodb data source.

        Parameters
        ----------
        connection_options : MongodbSourceConnectionOptions
            The connection options for the Mongodb data source.
        transformation_ctx : str, optional
            The transformation context for the dynamic frame. Defaults to "".

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.MONGODB.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )

    def write_dynamic_frame_to_mongodb(
        self: GlueContext,
        frame: DynamicFrame,
        connection_options: MongoDBSinkConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to Mongodb using the specified connection options.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to write to Mongodb.
        connection_options : MongodbSinkConnectionOptions
            The connection options for Mongodb.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        """
        return self.write_dynamic_frame_from_options(
            frame=frame,
            connection_type=ConnectionType.MONGODB.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )
