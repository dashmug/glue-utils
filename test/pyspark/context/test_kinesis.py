from unittest.mock import sentinel

from glue_utils.pyspark import (
    ConnectionType,
    GluePySparkContext,
)
from glue_utils.pyspark.connection_options import (
    KinesisSinkConnectionOptions,
    KinesisSourceConnectionOptions,
)


class TestGluePySparkContextForKinesis:
    def test_create_dynamic_frame(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_create_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.create_dynamic_frame_from_kinesis(
            connection_options=KinesisSourceConnectionOptions(
                streamARN="arn:aws:kinesis:us-east-2:777788889999:stream/fromOptionsStream",
                startingPosition="TRIM_HORIZON",
                inferSchema="true",
                classification="json",
            ),
            transformation_ctx="test",
        )

        mock_create_dynamic_frame_from_options.assert_called_once_with(
            connection_type=ConnectionType.KINESIS.value,
            connection_options={
                "streamARN": "arn:aws:kinesis:us-east-2:777788889999:stream/fromOptionsStream",
                "startingPosition": "TRIM_HORIZON",
                "inferSchema": "true",
                "classification": "json",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame

    def test_write_dynamic_frame(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_write_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.write_dynamic_frame_to_kinesis(
            frame=sentinel.dynamic_frame,
            connection_options=KinesisSinkConnectionOptions(
                streamARN="arn:aws:kinesis:us-east-2:777788889999:stream/fromOptionsStream",
            ),
            transformation_ctx="test",
        )

        mock_write_dynamic_frame_from_options.assert_called_once_with(
            frame=sentinel.dynamic_frame,
            connection_type=ConnectionType.KINESIS.value,
            connection_options={
                "streamARN": "arn:aws:kinesis:us-east-2:777788889999:stream/fromOptionsStream",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame
