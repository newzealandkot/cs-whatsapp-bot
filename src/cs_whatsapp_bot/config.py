import os
from dataclasses import dataclass


@dataclass
class Settings:
    whatsapp_verify_token: str


def load_settings() -> Settings:
    value = os.getenv("WHATSAPP_VERIFY_TOKEN")
    if value is None:
        raise RuntimeError("Missing required env var: WHATSAPP_VERIFY_TOKEN")
    return Settings(whatsapp_verify_token=value)


@dataclass
class SecuritySettings:
    whatsapp_app_secret: str


def load_security_settings() -> SecuritySettings:
    value = os.getenv("WHATSAPP_APP_SECRET")
    if value is None:
        raise RuntimeError("Missing required env var: WHATSAPP_APP_SECRET")
    return SecuritySettings(whatsapp_app_secret=value)
