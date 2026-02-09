import pytest


@pytest.mark.skip(reason="Covered by API health contract test")
def test_health_ok():
    assert True
