from __future__ import annotations

from dataclasses import dataclass, fields
from unittest.mock import patch

import pytest
from glue_utils import BaseOptions


@pytest.fixture
def mock_get_resolved_options():
    with patch("glue_utils.options.getResolvedOptions") as patched:
        yield patched


class TestBaseOptions:
    @pytest.mark.parametrize(
        ("args", "resolved_options"),
        [
            (
                ["--JOB_NAME", "test-job"],
                {"JOB_NAME": "test-job"},
            ),
            ([], {}),
        ],
    )
    def test_from_sys_argv(
        self,
        args,
        resolved_options,
        mock_get_resolved_options,
    ):
        with patch("sys.argv", ["test.py", *args]):
            mock_get_resolved_options.return_value = resolved_options
            options = BaseOptions.from_sys_argv()

            assert len(fields(options)) == 0


@dataclass
class Options(BaseOptions):
    connection_name: str
    source_database: str


class TestOptions:
    def test_from_sys_argv(self, mock_get_resolved_options):
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
            "connection_name": "test-connection",
            "source_database": "test-source-database",
        }

        options = Options.from_sys_argv()

        assert options.connection_name == "test-connection"
        assert options.source_database == "test-source-database"
        assert len(fields(options)) == 2

    def test_missing_options(self, mock_get_resolved_options):
        mock_get_resolved_options.return_value = {
            "connection_name": "test-connection",
        }

        with pytest.raises(TypeError):
            Options.from_sys_argv()


@dataclass
class NullableOptions(BaseOptions):
    connection_name: str
    source_database: str | None = None


class TestNullableOptions:
    def test_from_sys_argv(self, mock_get_resolved_options):
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
            "connection_name": "test-connection",
            "source_database": "test-source-database",
        }

        options = NullableOptions.from_sys_argv()

        assert options.connection_name == "test-connection"
        assert options.source_database == "test-source-database"
        assert len(fields(options)) == 2

    def test_missing_options(self, mock_get_resolved_options):
        mock_get_resolved_options.return_value = {
            "connection_name": "test-connection",
        }

        options = NullableOptions.from_sys_argv()

        assert options.connection_name == "test-connection"
        assert options.source_database is None
        assert len(fields(options)) == 2


@dataclass
class NullableOptionsWithDefaults(BaseOptions):
    connection_name: str = "my connection"
    source_database: str | None = "my source"


class TestNullableOptionsWithDefaults:
    def test_from_sys_argv(self, mock_get_resolved_options):
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
            "connection_name": "test-connection",
            "source_database": "test-source-database",
        }

        options = NullableOptionsWithDefaults.from_sys_argv()

        assert options.connection_name == "test-connection"
        assert options.source_database == "test-source-database"
        assert len(fields(options)) == 2

    def test_missing_options(self, mock_get_resolved_options):
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
        }

        options = NullableOptionsWithDefaults.from_sys_argv()

        assert options.connection_name == "my connection"
        assert options.source_database == "my source"
        assert len(fields(options)) == 2
