from __future__ import annotations  # noqa: D100

from typing import TYPE_CHECKING

from glue_utils.pyspark.connection_types import ConnectionType

if TYPE_CHECKING:
    from awsglue.context import GlueContext
    from awsglue.dynamicframe import DynamicFrame

    from glue_utils.pyspark.connection_options import (
        OpenSearchSinkConnectionOptions,
        OpenSearchSourceConnectionOptions,
    )


class OpenSearchMixin:
    """Mixin for working with OpenSearch connections."""

    def create_dynamic_frame_from_opensearch(
        self: GlueContext,
        connection_options: OpenSearchSourceConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Create a DynamicFrame from a OpenSearch data source.

        Parameters
        ----------
        connection_options : OpenSearchSourceConnectionOptions
            The connection options for the OpenSearch data source.
        transformation_ctx : str, optional
            The transformation context for the dynamic frame. Defaults to "".

        """
        return self.create_dynamic_frame_from_options(
            connection_type=ConnectionType.OPENSEARCH.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )

    def write_dynamic_frame_to_opensearch(
        self: GlueContext,
        frame: DynamicFrame,
        connection_options: OpenSearchSinkConnectionOptions,
        transformation_ctx: str = "",
    ) -> DynamicFrame:
        """Write a DynamicFrame to OpenSearch using the specified connection options.

        Parameters
        ----------
        frame : DynamicFrame
            The DynamicFrame to write to OpenSearch.
        connection_options : OpenSearchSinkConnectionOptions
            The connection options for OpenSearch.
        transformation_ctx : str, optional
            The transformation context. Defaults to "".

        """
        return self.write_dynamic_frame_from_options(
            frame=frame,
            connection_type=ConnectionType.OPENSEARCH.value,
            connection_options=connection_options,
            transformation_ctx=transformation_ctx,
        )
