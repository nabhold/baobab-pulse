"""``/research-missions`` — a minimal slice of the API boundary (item 60).

Not a complete resource (no listing, filtering, or pipeline-run endpoints
yet) — enough to prove the API -> application -> domain path end-to-end
through the headless boundary, per this scaffold's verification purpose.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from baobab_pulse.api.dependencies import get_research_mission_repository
from baobab_pulse.contracts.api.research_missions import (
    CreateResearchMissionRequest,
    ResearchMissionResponse,
)
from baobab_pulse.domain.research import ResearchMission
from baobab_pulse.domain.shared.identifiers import new_id
from baobab_pulse.infrastructure.persistence.in_memory_repositories import InMemoryRepository

router = APIRouter(prefix="/research-missions", tags=["research-missions"])


@router.post("", status_code=201)
async def create_research_mission(
    request: CreateResearchMissionRequest,
    repository: InMemoryRepository[ResearchMission] = Depends(get_research_mission_repository),
) -> ResearchMissionResponse:
    mission = ResearchMission(
        id=new_id("rms"),
        title=request.title,
        research_question=request.research_question,
        tenant_scope=request.tenant_scope,
        tenant_context=request.to_tenant_context(),
        classification=request.classification,
        confidence_requirement=request.confidence_requirement,
    )
    mission.check_tenant_context()
    await repository.add(mission)
    return ResearchMissionResponse.from_domain(mission)


@router.get("/{mission_id}")
async def get_research_mission(
    mission_id: str,
    repository: InMemoryRepository[ResearchMission] = Depends(get_research_mission_repository),
) -> ResearchMissionResponse:
    mission = await repository.get(mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail="research mission not found")
    return ResearchMissionResponse.from_domain(mission)
