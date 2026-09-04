"""FastAPI dependency wiring — the composition root for the API process.

Kept in one small module rather than scattered ``Depends()`` factories
throughout routers, so the wiring between ports and their infrastructure
implementations is visible in one place (item 128: "domain/application/
ports/infrastructure boundaries").
"""

from __future__ import annotations

from functools import lru_cache

from baobab_pulse.application.services.research_mission_service import ResearchMissionService
from baobab_pulse.configuration.settings import Settings
from baobab_pulse.domain.research import ResearchMission
from baobab_pulse.infrastructure.haystack.pipeline_adapter import HaystackPipelineAdapter
from baobab_pulse.infrastructure.persistence.connection import Database
from baobab_pulse.infrastructure.persistence.in_memory_repositories import InMemoryRepository


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_database() -> Database:
    return Database(get_settings().database_url)


@lru_cache
def get_research_mission_repository() -> InMemoryRepository[ResearchMission]:
    """In-memory for now (item 128 Phase 5: PostgreSQL repositories follow
    ADR-PULSE-011, not this scaffold)."""
    return InMemoryRepository()


@lru_cache
def get_research_mission_service() -> ResearchMissionService:
    return ResearchMissionService(pipeline_port=HaystackPipelineAdapter())
