"""The Baobab Tool Contract -> Haystack Tool adapter (item 20-24).

    Baobab Tool Contract -> Tool Adapter -> Haystack Tool

Prevents a Haystack ``Tool`` definition from ever becoming an
organisation-wide platform contract by itself (item 23) — the contract is
``BaobabToolContract``; ``to_haystack_tool`` is the only place it becomes a
``haystack.tools.Tool``.
"""
