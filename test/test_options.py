# ruff: noqa: UP045
from __future__ import annotations

import json
from dataclasses import dataclass, fields
from datetime import datetime, timezone
from typing import Any, ClassVar, Optional, cast
from unittest.mock import patch
from uuid import UUID

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


@dataclass
class CustomBooleanOptions(BaseOptions):
    """Custom options class with overridden boolean values."""

    # Override boolean conversion values
    TRUE_VALUES: ClassVar[set[str]] = {"ja", "oui", "si", "1"}
    FALSE_VALUES: ClassVar[set[str]] = {"nein", "non", "no", "0"}

    enabled: bool


class TestCustomBooleanOptions:
    """Test CustomBooleanOptions with overridden boolean values."""

    def test_custom_true_values(self, mock_get_resolved_options) -> None:
        """Test that custom TRUE_VALUES work correctly."""
        for true_val in ["ja", "oui", "si", "1"]:
            mock_get_resolved_options.return_value = {"enabled": true_val}
            options = CustomBooleanOptions.from_sys_argv()
            assert options.enabled is True

    def test_custom_false_values(self, mock_get_resolved_options) -> None:
        """Test that custom FALSE_VALUES work correctly."""
        for false_val in ["nein", "non", "no", "0"]:
            mock_get_resolved_options.return_value = {"enabled": false_val}
            options = CustomBooleanOptions.from_sys_argv()
            assert options.enabled is False

    def test_case_insensitive_custom_values(self, mock_get_resolved_options) -> None:
        """Test that custom boolean values are case insensitive."""
        # Test uppercase true values
        for true_val in ["JA", "OUI", "SI"]:
            mock_get_resolved_options.return_value = {"enabled": true_val}
            options = CustomBooleanOptions.from_sys_argv()
            assert options.enabled is True

        # Test uppercase false values
        for false_val in ["NEIN", "NON", "NO"]:
            mock_get_resolved_options.return_value = {"enabled": false_val}
            options = CustomBooleanOptions.from_sys_argv()
            assert options.enabled is False

    def test_whitespace_handling_custom_values(self, mock_get_resolved_options) -> None:
        """Test that custom boolean values handle whitespace correctly."""
        mock_get_resolved_options.return_value = {"enabled": " ja "}
        options = CustomBooleanOptions.from_sys_argv()
        assert options.enabled is True

        mock_get_resolved_options.return_value = {"enabled": " nein "}
        options = CustomBooleanOptions.from_sys_argv()
        assert options.enabled is False

    def test_default_boolean_values_not_accepted(
        self, mock_get_resolved_options
    ) -> None:
        """Test that default boolean values are not accepted in custom class."""
        # Default true values should not work
        mock_get_resolved_options.return_value = {"enabled": "true"}
        with pytest.raises(
            ValueError,
            match="Failed to convert field 'enabled' value 'true' to <class 'bool'>",
        ):
            CustomBooleanOptions.from_sys_argv()

        # Default false values should not work (except 'no' which is also in custom)
        mock_get_resolved_options.return_value = {"enabled": "false"}
        with pytest.raises(
            ValueError,
            match="Failed to convert field 'enabled' value 'false' to <class 'bool'>",
        ):
            CustomBooleanOptions.from_sys_argv()

    def test_invalid_custom_boolean_value(self, mock_get_resolved_options) -> None:
        """Test that invalid values raise appropriate errors."""
        mock_get_resolved_options.return_value = {"enabled": "invalid"}
        with pytest.raises(
            ValueError,
            match="Failed to convert field 'enabled' value 'invalid' to <class 'bool'>",
        ):
            CustomBooleanOptions.from_sys_argv()


@dataclass
class ExtendedBooleanOptions(BaseOptions):
    """Options class that extends boolean values instead of replacing them."""

    # Extend the boolean values by combining with parent values
    TRUE_VALUES: ClassVar[set[str]] = BaseOptions.TRUE_VALUES | {"on", "enabled"}
    FALSE_VALUES: ClassVar[set[str]] = BaseOptions.FALSE_VALUES | {"off", "disabled"}

    active: bool


class TestExtendedBooleanOptions:
    """Test ExtendedBooleanOptions with extended boolean values."""

    def test_extended_true_values(self, mock_get_resolved_options) -> None:
        """Test that extended TRUE_VALUES work correctly."""
        # Test new extended values
        for true_val in ["on", "enabled"]:
            mock_get_resolved_options.return_value = {"active": true_val}
            options = ExtendedBooleanOptions.from_sys_argv()
            assert options.active is True

        # Test original default values still work
        for true_val in BaseOptions.TRUE_VALUES:
            mock_get_resolved_options.return_value = {"active": true_val}
            options = ExtendedBooleanOptions.from_sys_argv()
            assert options.active is True

    def test_extended_false_values(self, mock_get_resolved_options) -> None:
        """Test that extended FALSE_VALUES work correctly."""
        # Test new extended values
        for false_val in ["off", "disabled"]:
            mock_get_resolved_options.return_value = {"active": false_val}
            options = ExtendedBooleanOptions.from_sys_argv()
            assert options.active is False

        # Test original default values still work
        for false_val in BaseOptions.FALSE_VALUES:
            mock_get_resolved_options.return_value = {"active": false_val}
            options = ExtendedBooleanOptions.from_sys_argv()
            assert options.active is False

    def test_case_insensitive_extended_values(self, mock_get_resolved_options) -> None:
        """Test that extended boolean values are case insensitive."""
        # Test uppercase extended true values
        for true_val in ["ON", "ENABLED"]:
            mock_get_resolved_options.return_value = {"active": true_val}
            options = ExtendedBooleanOptions.from_sys_argv()
            assert options.active is True

        # Test uppercase extended false values
        for false_val in ["OFF", "DISABLED"]:
            mock_get_resolved_options.return_value = {"active": false_val}
            options = ExtendedBooleanOptions.from_sys_argv()
            assert options.active is False

    def test_whitespace_handling_extended_values(
        self, mock_get_resolved_options
    ) -> None:
        """Test that extended boolean values handle whitespace correctly."""
        mock_get_resolved_options.return_value = {"active": " enabled "}
        options = ExtendedBooleanOptions.from_sys_argv()
        assert options.active is True

        mock_get_resolved_options.return_value = {"active": " disabled "}
        options = ExtendedBooleanOptions.from_sys_argv()
        assert options.active is False

    def test_all_boolean_combinations(self, mock_get_resolved_options) -> None:
        """Test that all boolean values (original + extended) work together."""
        all_true_values = BaseOptions.TRUE_VALUES | {"on", "enabled"}
        all_false_values = BaseOptions.FALSE_VALUES | {"off", "disabled"}

        # Test all true values
        for true_val in all_true_values:
            mock_get_resolved_options.return_value = {"active": true_val}
            options = ExtendedBooleanOptions.from_sys_argv()
            assert options.active is True, f"Failed for true value: {true_val}"

        # Test all false values
        for false_val in all_false_values:
            mock_get_resolved_options.return_value = {"active": false_val}
            options = ExtendedBooleanOptions.from_sys_argv()
            assert options.active is False, f"Failed for false value: {false_val}"

    def test_invalid_extended_boolean_value(self, mock_get_resolved_options) -> None:
        """Test that invalid values raise appropriate errors."""
        mock_get_resolved_options.return_value = {"active": "maybe"}
        with pytest.raises(
            ValueError,
            match="Failed to convert field 'active' value 'maybe' to <class 'bool'>",
        ):
            ExtendedBooleanOptions.from_sys_argv()


@dataclass
class OptionsWithCustomConverters(BaseOptions):
    """Options class that uses custom converters for values."""

    csv: list[str]
    json: dict[str, Any]
    created_at: datetime
    uuid: UUID

    def convert_csv(self, value: str) -> list[str]:
        """Convert a comma-separated string to a list of strings."""
        return [item.strip() for item in value.split(",") if item.strip()]

    def convert_json(self, value: str) -> dict[str, Any]:
        """Convert a JSON string to a dictionary."""
        return cast("dict[str, Any]", json.loads(value))

    def convert_created_at(self, value: str) -> datetime:
        """Convert a string to a datetime object."""
        return datetime.fromisoformat(value)

    def convert_uuid(self, value: str) -> UUID:
        """Convert a string to a UUID."""
        return UUID(value)


class TestOptionsWithCustomConverters:
    def test_from_sys_argv_with_custom_converters(
        self, mock_get_resolved_options
    ) -> None:
        mock_get_resolved_options.return_value = {
            "csv": "apple, banana, cherry",
            "json": '{"key1": "value1", "key2": 2}',
            "created_at": "2023-10-01T12:00:00+00:00",
            "uuid": "12345678-1234-5678-1234-567812345678",
        }

        options = OptionsWithCustomConverters.from_sys_argv()

        assert options.csv == ["apple", "banana", "cherry"]
        assert options.json == {"key1": "value1", "key2": 2}
        assert options.created_at == datetime(2023, 10, 1, 12, 0, tzinfo=timezone.utc)
        assert options.uuid == UUID("12345678-1234-5678-1234-567812345678")
