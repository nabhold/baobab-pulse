import pytest

from baobab_pulse.domain.shared.errors import TenantContextMissingError
from baobab_pulse.domain.shared.value_objects import TenantContext
from baobab_pulse.tenancy.context import bind_tenant_context, current_tenant_context, require_tenant_context


def test_require_tenant_context_raises_when_unbound() -> None:
    assert current_tenant_context() is None
    with pytest.raises(TenantContextMissingError):
        require_tenant_context()


def test_bind_tenant_context_scopes_to_the_block() -> None:
    context = TenantContext(tenant_id="tn_test01")
    with bind_tenant_context(context):
        assert require_tenant_context() is context
    assert current_tenant_context() is None
