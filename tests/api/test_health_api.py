from tests.assertions.api_assertions import assert_status


def test_health_endpoint(client):
    response = client.get("/health")
    assert_status(response, 200)
    assert response.json() == {"status": "ok"}
