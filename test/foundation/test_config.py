import pytest

from pylage.config import EnvironmentConfig


def test_environment_config_defaults(monkeypatch):
    monkeypatch.delenv("PYLAGE_HOST", raising=False)
    monkeypatch.delenv("PYLAGE_PORT", raising=False)
    monkeypatch.delenv("PYLAGE_ENV", raising=False)

    config = EnvironmentConfig.from_env()

    assert config.host == "127.0.0.1"
    assert config.port == 8000
    assert config.environment == "development"


def test_environment_config_reads_environment(monkeypatch):
    monkeypatch.setenv("PYLAGE_HOST", "0.0.0.0")
    monkeypatch.setenv("PYLAGE_PORT", "8765")
    monkeypatch.setenv("PYLAGE_ENV", "production")

    config = EnvironmentConfig.from_env()

    assert config.host == "0.0.0.0"
    assert config.port == 8765
    assert config.environment == "production"


def test_environment_config_normalizes_values(monkeypatch):
    monkeypatch.setenv("PYLAGE_HOST", "  0.0.0.0  ")
    monkeypatch.setenv("PYLAGE_PORT", " 8765 ")
    monkeypatch.setenv("PYLAGE_ENV", "  Production ")

    config = EnvironmentConfig.from_env()

    assert config.host == "0.0.0.0"
    assert config.port == 8765
    assert config.environment == "production"


def test_environment_config_rejects_invalid_port(monkeypatch):
    monkeypatch.setenv("PYLAGE_PORT", "not-a-port")

    with pytest.raises(ValueError, match="PYLAGE_PORT must be an integer"):
        EnvironmentConfig.from_env()


def test_environment_config_rejects_out_of_range_port(monkeypatch):
    monkeypatch.setenv("PYLAGE_PORT", "70000")

    with pytest.raises(ValueError, match="between 0 and 65535"):
        EnvironmentConfig.from_env()


def test_environment_config_rejects_empty_host(monkeypatch):
    monkeypatch.setenv("PYLAGE_HOST", "   ")

    with pytest.raises(ValueError, match="PYLAGE_HOST must not be empty"):
        EnvironmentConfig.from_env()


def test_environment_config_rejects_empty_environment(monkeypatch):
    monkeypatch.setenv("PYLAGE_ENV", "   ")

    with pytest.raises(ValueError, match="PYLAGE_ENV must not be empty"):
        EnvironmentConfig.from_env()
