from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Optional, Union
from unittest.mock import patch

import pytest

from glue_utils import BaseOptions
from glue_utils.options import UnsupportedTypeWarning


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
    ) -> None:
        with patch("sys.argv", ["test.py", *args]):
            mock_get_resolved_options.return_value = resolved_options
            options = BaseOptions.from_sys_argv()

            assert len(fields(options)) == 0


@dataclass
class Options(BaseOptions):
    connection_name: str
    source_database: str


class TestOptions:
    def test_from_sys_argv(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
            "connection_name": "test-connection",
            "source_database": "test-source-database",
        }

        options = Options.from_sys_argv()

        assert options.connection_name == "test-connection"
        assert options.source_database == "test-source-database"
        assert len(fields(options)) == 2

    def test_missing_options(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "connection_name": "test-connection",
        }

        with pytest.raises(TypeError):
            Options.from_sys_argv()


@dataclass
class NullableOptions(BaseOptions):
    connection_name: str
    source_database: Optional[str] = None


class TestNullableOptions:
    def test_from_sys_argv(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
            "connection_name": "test-connection",
            "source_database": "test-source-database",
        }

        options = NullableOptions.from_sys_argv()

        assert options.connection_name == "test-connection"
        assert options.source_database == "test-source-database"
        assert len(fields(options)) == 2

    def test_missing_options(self, mock_get_resolved_options) -> None:
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
    source_database: Optional[str] = "my source"


class TestNullableOptionsWithDefaults:
    def test_from_sys_argv(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
            "connection_name": "test-connection",
            "source_database": "test-source-database",
        }

        options = NullableOptionsWithDefaults.from_sys_argv()

        assert options.connection_name == "test-connection"
        assert options.source_database == "test-source-database"
        assert len(fields(options)) == 2

    def test_missing_options(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
        }

        options = NullableOptionsWithDefaults.from_sys_argv()

        assert options.connection_name == "my connection"
        assert options.source_database == "my source"
        assert len(fields(options)) == 2


class TestOptionsWithNonString:
    def test_warning_for_non_string_fields(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "JOB_NAME": "test-job",
            "start_timestamp": "1632960000",
            "end_timestamp": "1632963600",
            "pi": "3.14159",
        }

        with pytest.warns(UnsupportedTypeWarning) as warnings:

            @dataclass
            class OptionsWithNonStrings(BaseOptions):
                start_timestamp: int
                end_timestamp: int
                pi: Union[str, int, float]
                mode: str = "incremental"

            options = OptionsWithNonStrings.from_sys_argv()

        assert isinstance(options.start_timestamp, str)
        assert options.start_timestamp == "1632960000"

        assert isinstance(options.end_timestamp, str)
        assert options.end_timestamp == "1632963600"

        assert isinstance(options.pi, str)
        assert options.pi == "3.14159"

        assert isinstance(options.mode, str)
        assert options.mode == "incremental"

        assert len(fields(options)) == 4

        assert len(warnings) == 3
        assert (
            str(warnings[0].message)
            == '"start_timestamp" value is a string at runtime even if annotated to be "<class \'int\'>".'
        )
        assert (
            str(warnings[1].message)
            == '"end_timestamp" value is a string at runtime even if annotated to be "<class \'int\'>".'
        )
        assert (
            str(warnings[2].message)
            == '"pi" value is a string at runtime even if annotated to be "typing.Union[str, int, float]".'
        )
