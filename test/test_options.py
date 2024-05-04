from __future__ import annotations

from dataclasses import dataclass, fields

import pytest
from glue_utils import BaseOptions


class TestBaseOptions:
    @pytest.mark.parametrize(
        ("resolved_options", "job_name"),
        [
            ({"JOB_NAME": "test-job"}, "test-job"),
            ({}, ""),
            (None, ""),
        ],
    )
    def test_from_resolved_options(self, resolved_options, job_name):
        options = BaseOptions.from_resolved_options(resolved_options)

        assert len(fields(options)) == 0


@dataclass(frozen=True)
class Options(BaseOptions):
    connection_name: str
    source_database: str


class TestOptions:
    def test_from_resolved_options(self):
        resolved_options = {
            "JOB_NAME": "test-job",
            "connection_name": "test-connection",
            "source_database": "test-source-database",
        }

        options = Options.from_resolved_options(resolved_options)

        assert options.connection_name == "test-connection"
        assert options.source_database == "test-source-database"
        assert len(fields(options)) == 2

    def test_missing_options(self):
        resolved_options = {
            "connection_name": "test-connection",
        }

        with pytest.raises(TypeError):
            Options.from_resolved_options(resolved_options)


@dataclass(frozen=True)
class NullableOptions(BaseOptions):
    connection_name: str
    source_database: str | None = None


class TestNullableOptions:
    def test_from_resolved_options(self):
        resolved_options = {
            "JOB_NAME": "test-job",
            "connection_name": "test-connection",
            "source_database": "test-source-database",
        }

        options = NullableOptions.from_resolved_options(resolved_options)

        assert options.connection_name == "test-connection"
        assert options.source_database == "test-source-database"
        assert len(fields(options)) == 2

    def test_missing_options(self):
        resolved_options = {
            "connection_name": "test-connection",
        }

        options = NullableOptions.from_resolved_options(resolved_options)

        assert options.connection_name == "test-connection"
        assert options.source_database is None
        assert len(fields(options)) == 2


@dataclass(frozen=True)
class NullableOptionsWithDefaults(BaseOptions):
    connection_name: str = "my connection"
    source_database: str | None = "my source"


class TestNullableOptionsWithDefaults:
    def test_from_resolved_options(self):
        resolved_options = {
            "JOB_NAME": "test-job",
            "connection_name": "test-connection",
            "source_database": "test-source-database",
        }

        options = NullableOptionsWithDefaults.from_resolved_options(resolved_options)

        assert options.connection_name == "test-connection"
        assert options.source_database == "test-source-database"
        assert len(fields(options)) == 2

    def test_missing_options(self):
        resolved_options = {
            "JOB_NAME": "test-job",
        }

        options = NullableOptionsWithDefaults.from_resolved_options(resolved_options)

        assert options.connection_name == "my connection"
        assert options.source_database == "my source"
        assert len(fields(options)) == 2
