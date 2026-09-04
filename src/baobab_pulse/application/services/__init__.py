"""Baobab-owned application services (platform brief item 14).

These remain authoritative regardless of which AI orchestration framework
sits behind ``PipelinePort`` — Haystack pipelines invoke them through
adapters, they never re-implement this logic as Haystack Components.
"""
