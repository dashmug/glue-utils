from __future__ import annotations

from dataclasses import dataclass, fields
from typing import ClassVar, Optional
from unittest.mock import patch

import pytest

from glue_utils.pyspark import BaseOptions


@pytest.fixture
def mock_get_resolved_options():
    with patch("glue_utils.pyspark.options.getResolvedOptions") as patched:
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


@dataclass
class PrimitiveOptions(BaseOptions):
    port: int
    price: float
    enabled: bool
    name: str


class TestPrimitiveOptions:
    def test_from_sys_argv_converts_types(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "port": "5432",
            "price": "12.34",
            "enabled": "true",
            "name": "my-job",
        }
        options = PrimitiveOptions.from_sys_argv()
        assert isinstance(options.port, int)
        assert options.port == 5432
        assert isinstance(options.price, float)
        assert options.price == 12.34
        assert isinstance(options.enabled, bool)
        assert options.enabled is True
        assert isinstance(options.name, str)
        assert options.name == "my-job"

    @pytest.mark.parametrize(
        ("enabled_str", "expected"),
        [
            ("true", True),
            ("True", True),
            ("1", True),
            ("yes", True),
            ("y", True),
            ("t", True),
            ("false", False),
            ("False", False),
            ("0", False),
            ("no", False),
            ("n", False),
            ("f", False),
        ],
    )
    def test_bool_conversion_variants(
        self, mock_get_resolved_options, enabled_str, expected
    ) -> None:
        mock_get_resolved_options.return_value = {
            "port": "1234",
            "price": "1.0",
            "enabled": enabled_str,
            "name": "test",
        }
        options = PrimitiveOptions.from_sys_argv()
        assert options.enabled is expected

    def test_invalid_int_raises(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "port": "not-an-int",
            "price": "1.0",
            "enabled": "true",
            "name": "test",
        }
        with pytest.raises(
            ValueError,
            match="Failed to convert field 'port' value 'not-an-int' to <class 'int'>",
        ):
            PrimitiveOptions.from_sys_argv()

    def test_invalid_float_raises(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "port": "1234",
            "price": "not-a-float",
            "enabled": "true",
            "name": "test",
        }
        with pytest.raises(
            ValueError,
            match="Failed to convert field 'price' value 'not-a-float' to <class 'float'>",
        ):
            PrimitiveOptions.from_sys_argv()

    def test_invalid_bool_raises(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "port": "1234",
            "price": "1.0",
            "enabled": "not-a-bool",
            "name": "test",
        }
        with pytest.raises(
            ValueError,
            match="Failed to convert field 'enabled' value 'not-a-bool' to <class 'bool'>",
        ):
            PrimitiveOptions.from_sys_argv()

    def test_from_options_converts_types(self, mock_get_resolved_options) -> None:
        options = PrimitiveOptions.from_options(
            {
                "port": "8080",
                "price": "99.99",
                "enabled": "false",
                "name": "test-job",
            }
        )
        assert isinstance(options.port, int)
        assert options.port == 8080
        assert isinstance(options.price, float)
        assert options.price == 99.99
        assert isinstance(options.enabled, bool)
        assert options.enabled is False
        assert isinstance(options.name, str)
        assert options.name == "test-job"


@dataclass
class MixedOptionsWithDefaults(BaseOptions):
    host: str = "localhost"
    port: int = 5432
    timeout: float = 30.0
    debug: bool = False


class TestMixedOptionsWithDefaults:
    def test_with_all_values(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "host": "production.db",
            "port": "3306",
            "timeout": "60.5",
            "debug": "true",
        }
        options = MixedOptionsWithDefaults.from_sys_argv()
        assert options.host == "production.db"
        assert options.port == 3306
        assert options.timeout == 60.5
        assert options.debug is True

    def test_with_partial_values(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "port": "1234",
            "debug": "true",
        }
        options = MixedOptionsWithDefaults.from_sys_argv()
        assert options.host == "localhost"  # default value
        assert options.port == 1234  # converted from string
        assert options.timeout == 30.0  # default value
        assert options.debug is True  # converted from string

    def test_with_no_values(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {}
        options = MixedOptionsWithDefaults.from_sys_argv()
        assert options.host == "localhost"
        assert options.port == 5432
        assert options.timeout == 30.0
        assert options.debug is False


@dataclass
class OptionalPrimitiveOptions(BaseOptions):
    connection_name: str
    port: Optional[int] = None
    debug: Optional[bool] = None


class TestOptionalPrimitiveOptions:
    def test_with_optional_values(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "connection_name": "test-conn",
            "port": "5432",
            "debug": "true",
        }
        options = OptionalPrimitiveOptions.from_sys_argv()
        assert options.connection_name == "test-conn"
        assert isinstance(options.port, int)
        assert options.port == 5432
        assert isinstance(options.debug, bool)
        assert options.debug is True

    def test_with_missing_optional_values(self, mock_get_resolved_options) -> None:
        mock_get_resolved_options.return_value = {
            "connection_name": "test-conn",
        }
        options = OptionalPrimitiveOptions.from_sys_argv()
        assert options.connection_name == "test-conn"
        assert options.port is None
        assert options.debug is None


class TestCustomBooleanValues:
    """Test custom boolean conversion values."""

    def test_default_boolean_values(self) -> None:
        """Test that default TRUE_VALUES and FALSE_VALUES work correctly."""
        options = BaseOptions()

        # Test default TRUE_VALUES
        for true_val in BaseOptions.TRUE_VALUES:
            assert options.convert_to_bool(true_val) is True
            assert options.convert_to_bool(true_val.upper()) is True
            assert options.convert_to_bool(f" {true_val} ") is True  # with whitespace

        # Test default FALSE_VALUES
        for false_val in BaseOptions.FALSE_VALUES:
            assert options.convert_to_bool(false_val) is False
            assert options.convert_to_bool(false_val.upper()) is False
            assert options.convert_to_bool(f" {false_val} ") is False  # with whitespace

    def test_convert_to_bool_invalid_value(self) -> None:
        """Test convert_to_bool with invalid string values."""
        options = BaseOptions()
        with pytest.raises(ValueError, match="Cannot convert 'invalid' to bool"):
            options.convert_to_bool("invalid")

        with pytest.raises(ValueError, match="Cannot convert 'maybe' to bool"):
            options.convert_to_bool("maybe")


@dataclass
class CustomBooleanOptions(BaseOptions):
    """Custom options class with overridden boolean values."""

    # Override boolean conversion values
    TRUE_VALUES: ClassVar[set[str]] = {"ja", "oui", "si", "1"}
    FALSE_VALUES: ClassVar[set[str]] = {"nein", "non", "no", "0"}

    enabled: bool


@dataclass
class ExtendedBooleanOptions(BaseOptions):
    """Options class that extends boolean values instead of replacing them."""

    # Extend the boolean values by combining with parent values
    TRUE_VALUES: ClassVar[set[str]] = BaseOptions.TRUE_VALUES | {"on", "enabled"}
    FALSE_VALUES: ClassVar[set[str]] = BaseOptions.FALSE_VALUES | {"off", "disabled"}

    active: bool
