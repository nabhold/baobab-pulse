"""Infrastructure adapters implementing the ports in ``application.ports``.

Everything framework-, database-, and provider-specific lives here. Nothing
under ``baobab_pulse.domain`` or ``baobab_pulse.application`` imports
anything from this package — the dependency arrow only ever points inward.
"""
