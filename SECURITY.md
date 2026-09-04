# Security Policy

Baobab Pulse follows Nabhold's org-wide security policy and reporting
process.

## Reporting a vulnerability

**Do not open a public GitHub issue for a suspected vulnerability.**

Report privately to **security@nabhold.com** with:

- A description of the issue and its potential impact (e.g. tenant
  isolation failure, unauthorised evidence access, prompt injection leading
  to unintended tool/agent behaviour, dependency vulnerability).
- Steps to reproduce, including any relevant request payloads or
  configuration — with credentials/secrets redacted.
- The affected component (e.g. `api`, `infrastructure.haystack`,
  `ingestion`, a specific dependency).

We aim to acknowledge reports within 5 business days.

## Supported versions

Pulse is pre-1.0 and under active initial development. Security fixes land
on `main`; there is no maintained release branch yet.

## Scope-specific notes for Pulse

- **Tenant isolation**: `tenancy.context.require_tenant_context()` and
  `security.classification.may_access` are the structural enforcement
  points (item 49-50). A bypass of either is a high-severity finding.
- **AI/agent security**: see `docs/security/agent-and-tool-security.md` for
  what is and is not currently enforced around Haystack tools/agents. A
  prompt-injection path that reaches the system-role message, or a tool
  invocation that bypasses `BaobabToolContract`'s authority/side-effect
  checks, is a high-severity finding.
- **Secrets**: never commit `.env`, API keys, or database credentials. Use
  `.env.example` as the template; real values come from environment
  variables or the deployment platform's secret manager.
- **Dependencies**: `uv.lock` is the source of truth; `security-python.yml`
  (Bandit + pip-audit) and `security-codeql.yml` run in CI on every
  relevant change and weekly on a schedule.

## Baobab-wide policy

For anything not specific to this repository (disclosure timelines,
severity classification, incident-response process), see
`nabhold/shared`'s organisation-wide security documentation.
