from __future__ import annotations  # noqa: D100

from typing import TYPE_CHECKING

from glue_utils.pyspark.connection_types import ConnectionType

if TYPE_CHECKING:
    from awsglue.context import GlueContext
    from awsglue.dynamicframe import DynamicFrame

    from glue_utils.pyspark.connection_options import (
        KafkaSinkConnectionOptions,
        KafkaSourceConnectionOptions,
    )


class KafkaMixin:
    """Mixin for working with Kafka connections."""

    def create_dynamic_frame_from_kafka(
        self: GlueContext,
        connection_options: KafkaSourceConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from a Kafka data source.

        Parameters
        ----------
        connection_options : KafkaSourceConnectionOptions
            The connection options for the Kafka data source.
        transformation_ctx : str, optional
            The transformation context for the dynamic frame. Defaults to "".

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.KAFKA.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )

    def write_dynamic_frame_to_kafka(
        self: GlueContext,
        frame: DynamicFrame,
        connection_options: KafkaSinkConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to Kafka using the specified connection options.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to write to Kafka.
        connection_options : KafkaSinkConnectionOptions
            The connection options for Kafka.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        """
        return self.write_dynamic_frame_from_options(
            frame=frame,
            connection_type=ConnectionType.KAFKA.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )
