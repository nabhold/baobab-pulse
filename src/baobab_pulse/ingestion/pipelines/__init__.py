"""Raw-to-canonical normalisation (ADR-PULSE-003 §26 anti-corruption pipeline).

    source-specific format -> source adapter -> raw source record
        -> normaliser -> canonical observation

Not a Haystack pipeline — this is Pulse's own ingestion-side transformation,
independent of the intelligence-orchestration pipelines under
``infrastructure.haystack.pipelines``.
"""
