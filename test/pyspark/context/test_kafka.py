from unittest.mock import sentinel

from glue_utils.pyspark import (
    ConnectionType,
    GluePySparkContext,
)
from glue_utils.pyspark.connection_options import (
    KafkaSinkConnectionOptions,
    KafkaSourceConnectionOptions,
)


class TestGluePySparkContextForKafka:
    def test_create_dynamic_frame(
        self,
        glue_pyspark_context: GluePySparkContext,
        mock_create_dynamic_frame_from_options,
    ) -> None:
        dynamic_frame = glue_pyspark_context.create_dynamic_frame_from_kafka(
            connection_options=KafkaSourceConnectionOptions(
                connectionName="ConfluentKafka",
                topicName="kafka-auth-topic",
                startingOffsets="earliest",
                inferSchema="true",
                classification="json",
            ),
            transformation_ctx="test",
        )

        mock_create_dynamic_frame_from_options.assert_called_once_with(
            connection_type=ConnectionType.KAFKA.value,
            connection_options={
                "connectionName": "ConfluentKafka",
                "topicName": "kafka-auth-topic",
                "startingOffsets": "earliest",
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
        dynamic_frame = glue_pyspark_context.write_dynamic_frame_to_kafka(
            frame=sentinel.dynamic_frame,
            connection_options=KafkaSinkConnectionOptions(
                connectionName="ConfluentKafka",
                topicName="kafka-auth-topic",
                classification="json",
            ),
            transformation_ctx="test",
        )

        mock_write_dynamic_frame_from_options.assert_called_once_with(
            frame=sentinel.dynamic_frame,
            connection_type=ConnectionType.KAFKA.value,
            connection_options={
                "connectionName": "ConfluentKafka",
                "topicName": "kafka-auth-topic",
                "classification": "json",
            },
            transformation_ctx="test",
        )
        assert dynamic_frame == sentinel.dynamic_frame
