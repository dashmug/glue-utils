from __future__ import annotations  # noqa: D100

from typing import TYPE_CHECKING

from glue_utils.pyspark.connection_types import ConnectionType

if TYPE_CHECKING:
    from awsglue.context import GlueContext
    from awsglue.dynamicframe import DynamicFrame

    from glue_utils.pyspark.connection_options import (
        DocumentDBSinkConnectionOptions,
        DocumentDBSourceConnectionOptions,
    )


class DocumentDBMixin:
    """Mixin for working with DocumentDB connections."""

    def create_dynamic_frame_from_documentdb(
        self: GlueContext,
        connection_options: DocumentDBSourceConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from a DocumentDB data source.

        Parameters
        ----------
        connection_options : DocumentDBSourceConnectionOptions
            The connection options for the DocumentDB data source.
        transformation_ctx : str, optional
            The transformation context for the dynamic frame. Defaults to "".

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.DOCUMENTDB.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )

    def write_dynamic_frame_to_documentdb(
        self: GlueContext,
        frame: DynamicFrame,
        connection_options: DocumentDBSinkConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to DocumentDB using the specified connection options.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to write to DocumentDB.
        connection_options : DocumentDBSinkConnectionOptions
            The connection options for DocumentDB.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        """
        return self.write_dynamic_frame_from_options(
            frame=frame,
            connection_type=ConnectionType.DOCUMENTDB.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )
