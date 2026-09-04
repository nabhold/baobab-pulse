-- Foundational migration only (item 63, 128 Phase 5): proves the migration
-- mechanism works and stakes out the schema boundaries ADR-PULSE-002 §93
-- illustrates (source, ingestion, evidence, intelligence, decision, model).
--
-- The full physical data model — tables, partitioning, row-level security
-- — is deliberately NOT defined here. That is ADR-PULSE-011's job
-- (PostgreSQL Physical Architecture); inventing it now would bake
-- unreviewed physical decisions into the repository ahead of that ADR.

CREATE SCHEMA IF NOT EXISTS source;
CREATE SCHEMA IF NOT EXISTS ingestion;
CREATE SCHEMA IF NOT EXISTS evidence;
CREATE SCHEMA IF NOT EXISTS intelligence;
CREATE SCHEMA IF NOT EXISTS decision;
CREATE SCHEMA IF NOT EXISTS model;

-- The transactional outbox (item 55-58) — the one table this scaffold does
-- commit to, since PULSE-016/item 58 explicitly ask the persistence layer
-- to support it. Consumers relay rows to the org event bus at-least-once
-- and mark them delivered; nothing here dictates *which* relay mechanism.
CREATE TABLE IF NOT EXISTS intelligence.outbox (
    id UUID PRIMARY KEY,
    event_type TEXT NOT NULL,
    envelope JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    delivered_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS outbox_undelivered_idx
    ON intelligence.outbox (created_at)
    WHERE delivered_at IS NULL;
