"""Binds a provider-neutral ``ModelVersion`` to a concrete Haystack Generator.

Pulse SHALL remain model-provider neutral (item 37) — this is the only place
a provider name (``"openai"``, ``"anthropic"``, ``"mock"``) is turned into an
actual Haystack Generator/ChatGenerator class.
"""
