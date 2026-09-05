"""``POST /evidence/search`` at the HTTP boundary (Qdrant refactor item 42,
44): a request with no ``X-Baobab-Tenant-Id`` header fails closed with 400
``TENANT_CONTEXT_MISSING`` rather than reaching Qdrant with an unrestricted
query, and a bound tenant with no matching evidence gets a normal, empty
200 response — never a raw Qdrant/Haystack exception.

Uses embedded (``:memory:``) Qdrant, so no live Qdrant server is required.
``dependencies.py`` wires its singletons with ``@lru_cache`` (item 128); each
test clears and rebuilds them under its own monkeypatched environment so
tests never see another test's (or another test file's) cached settings.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from baobab_pulse.api import dependencies

_CACHED_DEPENDENCIES = (
    dependencies.get_settings,
    dependencies.get_database,
    dependencies.get_embedding_port,
    dependencies.get_qdrant_evidence_store,
    dependencies.get_evidence_repository,
    dependencies.get_evidence_retrieval_service,
    dependencies.get_research_mission_repository,
    dependencies.get_research_mission_service,
)


@pytest.fixture
def api_client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("PULSE_QDRANT_URL", "")
    monkeypatch.setenv("PULSE_QDRANT_LOCATION", ":memory:")
    # No real PostgreSQL is required for these tests (missing tenant context
    # never reaches it; the empty-result search never calls hydration) —
    # point at an unreachable address so a stray connection attempt fails
    # fast rather than hanging.
    monkeypatch.setenv("PULSE_DATABASE_URL", "postgresql://pulse:pulse@localhost:1/baobab_pulse")
    for cached in _CACHED_DEPENDENCIES:
        cached.cache_clear()

    from baobab_pulse.api.main import create_app

    app = create_app()
    with TestClient(app) as client:
        yield client

    for cached in _CACHED_DEPENDENCIES:
        cached.cache_clear()


def test_search_with_no_tenant_context_fails_closed_with_400(api_client: TestClient) -> None:
    response = api_client.post("/evidence/search", json={"query_text": "coffee exports"})

    assert response.status_code == 400
    body = response.json()
    assert body["code"] == "TENANT_CONTEXT_MISSING"
    assert body["retryable"] is False


def test_search_with_a_bound_tenant_and_no_matching_evidence_returns_an_empty_200(
    api_client: TestClient,
) -> None:
    response = api_client.post(
        "/evidence/search",
        json={"query_text": "coffee exports"},
        headers={"X-Baobab-Tenant-Id": "tn_test01"},
    )

    assert response.status_code == 200
    assert response.json() == {"candidates": []}


def test_search_request_rejects_an_empty_query_text(api_client: TestClient) -> None:
    response = api_client.post(
        "/evidence/search", json={"query_text": ""}, headers={"X-Baobab-Tenant-Id": "tn_test01"}
    )

    assert response.status_code == 422
