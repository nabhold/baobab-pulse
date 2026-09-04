"""The Evidence -> Haystack Document translation boundary (item 28, 30-31).

    Canonical Evidence
           |
           v
    Retrieval Projection        <- build_documents() / EvidenceRetrievalProjection
           |
           v
    Haystack Document Store / Retriever

Every ``Document`` this module produces carries enough metadata
(``evidence_id``, ``object_type``, ``object_id``, ``tenant_scope``,
``classification``) to recover provenance, classification and tenant
context (item 28) — the projection is a *view*, never a place where that
context can be silently dropped.

Classification filtering happens here (item 50: filtering occurs before
unauthorised evidence enters model context), via
``security.classification.may_access`` — a retriever built from this
projection cannot return anything the caller was not already cleared for,
regardless of what any prompt says.
"""

from __future__ import annotations

from collections.abc import Mapping

from haystack import Document
from haystack.document_stores.in_memory import InMemoryDocumentStore

from baobab_pulse.domain.evidence import EvidenceSet
from baobab_pulse.domain.shared.enums import Classification
from baobab_pulse.security.classification import may_access


def build_documents(
    evidence_set: EvidenceSet,
    evidence_text: Mapping[str, str],
    *,
    requester_clearance: Classification = Classification.BAOBAB_INTERNAL,
) -> list[Document]:
    """Translate an :class:`EvidenceSet` into retrievable ``Document``\\ s.

    ``evidence_text`` supplies the actual snippet content for each
    ``Evidence.id`` — Evidence itself only *references* other canonical
    objects (item 27: Evidence never becomes the canonical record), so the
    caller (an application service reading the referenced Observations/
    SourceDocuments) is responsible for resolving the text.
    """
    documents: list[Document] = []
    for entry in evidence_set.entries:
        if not may_access(
            requester_clearance=requester_clearance, object_classification=evidence_set.classification
        ):
            continue
        text = evidence_text.get(entry.id)
        if text is None:
            continue
        documents.append(
            Document(
                id=entry.id,
                content=text,
                meta={
                    "evidence_id": entry.id,
                    "evidence_set_id": evidence_set.id,
                    "object_type": entry.referenced_object.object_type,
                    "object_id": entry.referenced_object.object_id,
                    "direction": entry.direction.value,
                    "quality": entry.quality.value,
                    "tenant_scope": evidence_set.tenant_scope.value,
                    "classification": evidence_set.classification.value,
                },
            )
        )
    return documents


class EvidenceRetrievalProjection:
    """A rebuildable, in-memory retrieval projection over one EvidenceSet.

    Not canonical storage (item 29) — call :meth:`rebuild` any time the
    underlying EvidenceSet changes; nothing here is the source of truth.
    """

    def __init__(self) -> None:
        self._store = InMemoryDocumentStore()

    def rebuild(
        self,
        evidence_set: EvidenceSet,
        evidence_text: Mapping[str, str],
        *,
        requester_clearance: Classification = Classification.BAOBAB_INTERNAL,
    ) -> None:
        self._store = InMemoryDocumentStore()
        documents = build_documents(evidence_set, evidence_text, requester_clearance=requester_clearance)
        if documents:
            self._store.write_documents(documents)

    @property
    def document_store(self) -> InMemoryDocumentStore:
        return self._store
