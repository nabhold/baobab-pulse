# Known issue: `.nabhold/environment.yaml` vs. Foundation Repository Gates

**Status:** Resolved upstream. `nabhold/shared#14` fixed the comparison
(`String#start_with?` -> a real `Gem::Version` `>=` floor check) and
merged as `nabhold/shared@2da1a429602d2f1421c498d412bb6c65a5626127`; this
repository's `.github/workflows/foundation.yml` now pins that commit (no
tagged release covers it yet — repin to a tag once `nabhold/shared` cuts
one that includes it). The history below is kept for context on how the
conflict was originally diagnosed and why neither side was silently
patched in the interim.

Originally flagged per the platform brief's "do not work around a
shared-contract conflict silently" rule (item 135): this repository had no
authority to change `nabhold/shared`, and rolling this repository's own
declaration backward would have misrepresented its actual `baobab-dev`
requirement, so neither side was silently patched at the time.

## The conflict

`.nabhold/environment.yaml` (already committed before this scaffolding
pass, in the `feat/foundation-4-github-codespaces` PR) declares:

```yaml
environment:
  profile: "full"
  minimum_version: "1.3.0"
```

`nabhold/shared`'s `foundation-repository-gates.yml` (as of tag `v1.2.0`,
commit `38defb11aacd95a6f68b7db8026fe336417a2af6`) validates the `full`
profile with:

```ruby
PROFILE_BASELINES = {
  "full" => { minimum: "1.2.6", tag: ->(v) { "ghcr.io/nabhold/baobab-dev:#{v}" } },
  ...
}
minimum = declaration.dig("environment", "minimum_version").to_s
abort "..." unless minimum.start_with?(baseline[:minimum])
```

`"1.3.0".start_with?("1.2.6")` is `false` — this check is a literal string
prefix match, not a version-floor (`>=`) comparison. As written, any
`full`-profile repository declaring a `minimum_version` newer than
`"1.2.6"` (verbatim) fails this specific check, which appears to be a
defect in the *comparison logic itself* rather than an intentional
"exactly 1.2.6" requirement — the surrounding comment describes it as a
"floor," and floors are normally `>=`, not string-prefix.

## Options

1. **Fix the comparison in `nabhold/shared`** (`foundation-repository-gates.yml`)
   to a real semantic-version `>=` comparison instead of `String#start_with?`.
   This is the most correct fix and benefits every `full`-profile consumer,
   not just this repository.
2. **Bump the `full` baseline's `minimum` value** in `nabhold/shared` to
   `"1.3.0"` (matching the `PROFILE_BASELINES` maintenance note's own
   guidance for a deliberate floor bump) — narrower fix, same file.
3. Do nothing here and accept that the `repository-contract` job of
   Foundation Repository Gates currently fails for `baobab-pulse` until (1)
   or (2) lands upstream.

## Resolution

Option 1 was implemented: [`nabhold/shared#14`](https://github.com/nabhold/shared/pull/14)
replaced the `String#start_with?` check with a real `Gem::Version` `>=`
comparison (plus a clear, explicit error for an unparseable
`minimum_version`), verified against three cases — a release above the
floor, a release below the floor, and an unparseable version string —
before merging. It merged as
`nabhold/shared@2da1a429602d2f1421c498d412bb6c65a5626127`, and this
repository's `.github/workflows/foundation.yml` now pins that commit.

This repository's own `.nabhold/environment.yaml`/`.devcontainer/devcontainer.json`
were never changed to work around this (`minimum_version: "1.3.0"`, image
`ghcr.io/nabhold/baobab-dev:1.3.0`) — that declaration was accurate for
what this repository actually needs throughout; it was the shared gate's
comparison that needed correcting, not this repository's stated
requirement.
