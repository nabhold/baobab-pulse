"""FastAPI dependency wiring — the composition root for the API process.

Kept in one small module rather than scattered ``Depends()`` factories
throughout routers, so the wiring between ports and their infrastructure
implementations is visible in one place (item 128: "domain/application/
ports/infrastructure boundaries").
"""

from __future__ import annotations

from functools import lru_cache

from baobab_pulse.application.ports.vector_projection_port import ProjectionCollection
from baobab_pulse.application.services.evidence_retrieval_service import EvidenceRetrievalService
from baobab_pulse.application.services.research_mission_service import ResearchMissionService
from baobab_pulse.configuration.settings import Settings
from baobab_pulse.domain.research import ResearchMission
from baobab_pulse.infrastructure.haystack.document_stores.qdrant_projection_store import (
    QdrantEvidenceProjectionStore,
    resolve_collection_name,
)
from baobab_pulse.infrastructure.haystack.embedders.embedding_adapter import (
    HaystackEmbeddingAdapter,
    build_document_embedder,
    build_text_embedder,
)
from baobab_pulse.infrastructure.haystack.pipeline_adapter import HaystackPipelineAdapter
from baobab_pulse.infrastructure.persistence.connection import Database
from baobab_pulse.infrastructure.persistence.evidence_repository import PostgresEvidenceSetRepository
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


@lru_cache
def get_evidence_repository() -> PostgresEvidenceSetRepository:
    return PostgresEvidenceSetRepository(get_database())


@lru_cache
def get_embedding_port() -> HaystackEmbeddingAdapter:
    settings = get_settings()
    return HaystackEmbeddingAdapter(
        text_embedder=build_text_embedder(
            settings.embedding_provider, dimension=settings.embedding_dimension, model=settings.embedding_model_id
        ),
        document_embedder=build_document_embedder(
            settings.embedding_provider, dimension=settings.embedding_dimension, model=settings.embedding_model_id
        ),
        model_id=f"{settings.embedding_provider}:{settings.embedding_model_id}",
        model_version="1",
    )


@lru_cache
def get_qdrant_evidence_store() -> QdrantEvidenceProjectionStore:
    settings = get_settings()
    return QdrantEvidenceProjectionStore(
        get_embedding_port(),
        collection_name=resolve_collection_name(
            ProjectionCollection.EVIDENCE,
            prefix=settings.qdrant_collection_prefix,
            version=settings.qdrant_evidence_collection_version,
        ),
        url=settings.qdrant_url,
        location=settings.qdrant_location,
        api_key=settings.qdrant_api_key.get_secret_value() if settings.qdrant_api_key else None,
        https=settings.qdrant_tls,
        timeout=settings.qdrant_timeout_seconds,
    )


@lru_cache
def get_evidence_retrieval_service() -> EvidenceRetrievalService:
    return EvidenceRetrievalService(
        semantic_retrieval=get_qdrant_evidence_store(), hydration=get_evidence_repository()
    )
