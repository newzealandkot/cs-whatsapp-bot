import pytest

from src.cs_whatsapp_bot import config

BLANK_VALUES = [None, "", "   ", "\t\n"]


def _set_env(monkeypatch, name, value):
    if value is None:
        monkeypatch.delenv(name, raising=False)
    else:
        monkeypatch.setenv(name, value)


@pytest.mark.parametrize("raw_value", BLANK_VALUES)
def test_load_settings_rejects_blank_verify_token(monkeypatch, raw_value):
    _set_env(monkeypatch, "WHATSAPP_VERIFY_TOKEN", raw_value)
    with pytest.raises(RuntimeError):
        config.load_settings()


def test_load_settings_accepts_non_blank_verify_token(monkeypatch):
    monkeypatch.setenv("WHATSAPP_VERIFY_TOKEN", "real-token")
    settings = config.load_settings()
    assert settings.whatsapp_verify_token == "real-token"


@pytest.mark.parametrize("raw_value", BLANK_VALUES)
def test_load_security_settings_rejects_blank_app_secret(monkeypatch, raw_value):
    _set_env(monkeypatch, "WHATSAPP_APP_SECRET", raw_value)
    with pytest.raises(RuntimeError):
        config.load_security_settings()


def test_load_security_settings_accepts_non_blank_app_secret(monkeypatch):
    monkeypatch.setenv("WHATSAPP_APP_SECRET", "real-secret")
    settings = config.load_security_settings()
    assert settings.whatsapp_app_secret == "real-secret"


@pytest.mark.parametrize("raw_value", BLANK_VALUES)
def test_load_database_url_rejects_blank_value(monkeypatch, raw_value):
    _set_env(monkeypatch, "DATABASE_URL", raw_value)
    with pytest.raises(RuntimeError):
        config.load_database_url()


def test_load_database_url_accepts_non_blank_value(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "app.db")
    assert config.load_database_url() == "app.db"


@pytest.mark.parametrize("raw_value", BLANK_VALUES)
def test_load_sender_settings_rejects_blank_access_token(monkeypatch, raw_value):
    monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "123456")
    _set_env(monkeypatch, "WHATSAPP_ACCESS_TOKEN", raw_value)
    with pytest.raises(RuntimeError):
        config.load_sender_settings()


@pytest.mark.parametrize("raw_value", BLANK_VALUES)
def test_load_sender_settings_rejects_blank_phone_number_id(monkeypatch, raw_value):
    monkeypatch.setenv("WHATSAPP_ACCESS_TOKEN", "real-access-token")
    _set_env(monkeypatch, "WHATSAPP_PHONE_NUMBER_ID", raw_value)
    with pytest.raises(RuntimeError):
        config.load_sender_settings()


def test_load_sender_settings_accepts_non_blank_required_values(monkeypatch):
    monkeypatch.setenv("WHATSAPP_ACCESS_TOKEN", "real-access-token")
    monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "123456")
    monkeypatch.delenv("WHATSAPP_API_VERSION", raising=False)
    settings = config.load_sender_settings()
    assert settings.whatsapp_access_token == "real-access-token"
    assert settings.whatsapp_phone_number_id == "123456"


def test_load_sender_settings_defaults_api_version_when_not_set(monkeypatch):
    monkeypatch.setenv("WHATSAPP_ACCESS_TOKEN", "real-access-token")
    monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "123456")
    monkeypatch.delenv("WHATSAPP_API_VERSION", raising=False)
    settings = config.load_sender_settings()
    assert settings.whatsapp_api_version == "v26.0"


def test_load_sender_settings_uses_custom_api_version_when_set(monkeypatch):
    monkeypatch.setenv("WHATSAPP_ACCESS_TOKEN", "real-access-token")
    monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "123456")
    monkeypatch.setenv("WHATSAPP_API_VERSION", "v20.0")
    settings = config.load_sender_settings()
    assert settings.whatsapp_api_version == "v20.0"
