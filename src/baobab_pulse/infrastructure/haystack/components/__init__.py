"""Pulse-authored Haystack components (platform brief item 13).

Narrow technical capabilities only — domain logic (confidence composition,
quality assessment, entity resolution) stays in ``application.services`` and
is *called by* these components, never re-implemented inside them (item 14).
Only the two reference components needed to prove the pipeline architecture
exist here; the extension mechanism (write a class, decorate it with
``@component``, wire it into a pipeline in ``pipelines/``) is what item 13
asks this scaffold to establish — not an exhaustive component catalogue.
"""
