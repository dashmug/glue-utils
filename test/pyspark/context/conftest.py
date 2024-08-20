from unittest.mock import patch, sentinel

import pytest
from pyspark import SparkContext

from glue_utils.pyspark.context import GluePySparkContext


@pytest.fixture(scope="package")
def glue_pyspark_context():
    sc = SparkContext.getOrCreate()
    yield GluePySparkContext(sc)
    sc.stop()


@pytest.fixture
def mock_create_dynamic_frame_from_options(glue_pyspark_context):
    with patch.object(
        glue_pyspark_context,
        "create_dynamic_frame_from_options",
        wraps=glue_pyspark_context.create_dynamic_frame_from_options,
        return_value=sentinel.dynamic_frame,
    ) as patched:
        yield patched


@pytest.fixture
def mock_write_dynamic_frame_from_options(glue_pyspark_context):
    with patch.object(
        glue_pyspark_context,
        "write_dynamic_frame_from_options",
        wraps=glue_pyspark_context.write_dynamic_frame_from_options,
        return_value=sentinel.dynamic_frame,
    ) as patched:
        yield patched
