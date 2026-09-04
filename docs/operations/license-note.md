# Known issue: this repository's LICENSE does not match the org convention

**Status:** Open, not resolved by this scaffold — a licensing choice is not
an engineering decision this scaffolding pass has authority to make (item
125: "Preserve the Nabhold organisation's established repository licensing
policy unless instructed otherwise").

## What was found

`baobab-pulse`'s committed `LICENSE` file (present since the repository's
very first commit, before this scaffolding pass) is the **GNU GPLv3** full
text. Every other inspected `nabhold/*` engine repository uses a different
license:

| Repository | License |
|---|---|
| `nabhold/baobab-cp` | Apache License 2.0 |
| `nabhold/baobab-dev` | Apache License 2.0 |
| `nabhold/engine-template` | Apache License 2.0 |
| `nabhold/shared` | MIT |
| `nabhold/baobab-pulse` (this repo) | **GNU GPLv3** |

`nabhold/engine-template` — the org's own scaffold for new engine
repositories — ships Apache-2.0. GPLv3 is a strong-copyleft license with
distribution/derivative-work obligations that are unusual for an internal
enterprise platform engine and inconsistent with every other engine
repository inspected; this looks like a copy-paste error in `baobab-pulse`'s
initial commit rather than a deliberate choice.

## What this scaffold did

`pyproject.toml`'s `license` field was set to `"GPL-3.0-or-later"` so it is
at least *consistent* with the LICENSE file actually committed — the
alternative (leaving it declared as `"Apache-2.0"`, as an earlier draft of
this scaffold briefly did before this was caught) would have made the
package metadata claim a license the repository does not actually grant,
which is worse than an org-convention mismatch.

## Recommendation

Confirm with whoever owns Nabhold's licensing policy whether `baobab-pulse`
should in fact carry a different license than every sibling engine
repository. If not (the likely case), replace `LICENSE` with the Apache
License 2.0 text (matching `nabhold/engine-template`) in a dedicated,
deliberate change — not silently as a side effect of unrelated scaffolding
work — and update `pyproject.toml`'s `license` field to `"Apache-2.0"` in
the same change.
