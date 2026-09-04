"""Twelve-factor, fail-fast Pulse configuration (item 118-119).

Invalid production configuration SHALL fail fast with actionable errors —
``pydantic-settings`` gives this for free: constructing :class:`Settings`
raises ``pydantic.ValidationError`` naming exactly which environment
variable is missing or malformed, rather than the process starting and
failing confusingly on first use.

Provider credentials (``*_API_KEY``) are optional at this layer — the core
test suite and the deterministic reference pipeline never require one
(req. 96); a real ``ModelExecutionPort`` adapter that needs one fails
clearly at the point it is actually selected, not at settings-load time for
every deployment regardless of which provider it uses.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PULSE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: Environment = Environment.LOCAL
    service_name: str = "baobab-pulse"
    log_level: str = "INFO"

    database_url: str = Field(
        default="postgresql://pulse:pulse@localhost:5432/baobab_pulse",
        description="PostgreSQL 17 connection string (ADR-PULSE parent spec §44).",
    )

    object_storage_endpoint: str | None = None
    object_storage_bucket: str = "baobab-pulse-evidence"
    object_storage_access_key: SecretStr | None = None
    object_storage_secret_key: SecretStr | None = None

    otel_exporter_otlp_endpoint: str | None = None
    otel_traces_enabled: bool = False

    openai_api_key: SecretStr | None = None
    anthropic_api_key: SecretStr | None = None

    api_host: str = "0.0.0.0"  # noqa: S104 -- container-internal bind, fronted by an ingress/load balancer
    api_port: int = 8000

    def is_production(self) -> bool:
        return self.environment == Environment.PRODUCTION
