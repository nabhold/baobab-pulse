"""Source and DataSource — the "Source Management" bounded context.

ADR-PULSE-002 §2.1 treats ``Source`` + ``DataSource`` as one bounded context;
``Source`` is the aggregate root, ``DataSource`` a subordinate entity that MAY
become its own aggregate root later if operational scale justifies it
(ADR-PULSE-002). Field lists: ARCH-PULSE-CIM-001 §11-15.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import ConfigDict

from baobab_pulse.domain.shared.base import CanonicalEntity
from baobab_pulse.domain.shared.value_objects import QualityProfile


class SourceType(StrEnum):
    """ARCH-PULSE-CIM-001 §12."""

    GOVERNMENT = "GOVERNMENT"
    CENTRAL_BANK = "CENTRAL_BANK"
    INTERNATIONAL_ORGANISATION = "INTERNATIONAL_ORGANISATION"
    NEWS_ORGANISATION = "NEWS_ORGANISATION"
    MARKET_DATA_PROVIDER = "MARKET_DATA_PROVIDER"
    WEATHER_PROVIDER = "WEATHER_PROVIDER"
    REGISTRY = "REGISTRY"
    RESEARCH_INSTITUTION = "RESEARCH_INSTITUTION"
    COMMERCIAL_PROVIDER = "COMMERCIAL_PROVIDER"
    BAOBAB_ENGINE = "BAOBAB_ENGINE"
    TENANT = "TENANT"
    MANUAL = "MANUAL"
    OTHER = "OTHER"


class DataDomain(StrEnum):
    """ARCH-PULSE-CIM-001 §15 — the eleven first-class external intelligence
    domains from ARCH-PULSE-001 §5, plus the internal Baobab engine domains."""

    FX = "FX"
    COMMODITY = "COMMODITY"
    WEATHER = "WEATHER"
    TRADE = "TRADE"
    CUSTOMS = "CUSTOMS"
    MACROECONOMIC = "MACROECONOMIC"
    MARKET_PRICE = "MARKET_PRICE"
    COMPANY_REGISTRY = "COMPANY_REGISTRY"
    GEOSPATIAL = "GEOSPATIAL"
    GOVERNMENT_OPEN_DATA = "GOVERNMENT_OPEN_DATA"
    NEWS = "NEWS"
    REGULATORY = "REGULATORY"
    CONTENT = "CONTENT"
    COMMERCE = "COMMERCE"
    ERP = "ERP"
    OTHER = "OTHER"


class SourceStatus(StrEnum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    RETIRED = "RETIRED"


class Source(CanonicalEntity):
    """Aggregate root. AGG-PULSE invariants: ``source_id`` immutable; name
    non-empty; type/status valid; trust assessments versioned where material."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["source"] = "source"
    name: str
    source_type: SourceType
    organisation_reference: str | None = None
    jurisdiction: str | None = None
    authority_class: str | None = None
    website: str | None = None
    trust_profile: QualityProfile = QualityProfile()
    status: SourceStatus = SourceStatus.ACTIVE
    metadata: dict[str, str] = {}


class DataSource(CanonicalEntity):
    """Subordinate to :class:`Source` (``Source 1 ─── * DataSource``)."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["data_source"] = "data_source"
    source_id: str
    name: str
    data_domain: DataDomain
    transport: str | None = None
    endpoint_reference: str | None = None
    authentication_type: str | None = None
    refresh_policy: str | None = None
    licence_profile: str | None = None
    schema_profile: str | None = None
    status: SourceStatus = SourceStatus.ACTIVE
    metadata: dict[str, str] = {}
