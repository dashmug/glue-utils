from __future__ import annotations  # noqa: D100

from typing import TYPE_CHECKING

from glue_utils.pyspark.connection_types import ConnectionType

if TYPE_CHECKING:
    from awsglue.context import GlueContext
    from awsglue.dynamicframe import DynamicFrame

    from glue_utils.pyspark.connection_options import (
        KinesisSinkConnectionOptions,
        KinesisSourceConnectionOptions,
    )


class KinesisMixin:
    """Mixin for working with Kinesis connections."""

    def create_dynamic_frame_from_kinesis(
        self: GlueContext,
        connection_options: KinesisSourceConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from a Kinesis data source.

        Parameters
        ----------
        connection_options : KinesisSourceConnectionOptions
            The connection options for the Kinesis data source.
        transformation_ctx : str, optional
            The transformation context for the dynamic frame. Defaults to "".

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.KINESIS.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )

    def write_dynamic_frame_to_kinesis(
        self: GlueContext,
        frame: DynamicFrame,
        connection_options: KinesisSinkConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to Kinesis using the specified connection options.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to write to Kinesis.
        connection_options : KinesisSinkConnectionOptions
            The connection options for Kinesis.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        """
        return self.write_dynamic_frame_from_options(
            frame=frame,
            connection_type=ConnectionType.KINESIS.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )
