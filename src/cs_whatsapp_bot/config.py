import os
from dataclasses import dataclass


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise RuntimeError(f"Missing required env var: {name}")
    return value


@dataclass
class Settings:
    whatsapp_verify_token: str


def load_settings() -> Settings:
    return Settings(whatsapp_verify_token=_require_env("WHATSAPP_VERIFY_TOKEN"))


@dataclass
class SecuritySettings:
    whatsapp_app_secret: str


def load_security_settings() -> SecuritySettings:
    return SecuritySettings(whatsapp_app_secret=_require_env("WHATSAPP_APP_SECRET"))


def load_database_url() -> str:
    return _require_env("DATABASE_URL")
