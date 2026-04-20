from fastapi.testclient import TestClient
from main import app


def test_get_guitars():
    client = TestClient(app)
    """
    Test that the /guitars endpoint returns status 200 and contains the expected guitars.
    """
    response = client.get("/guitars")
    
    # Assert status code is 200
    assert response.status_code == 200
    
    # Assert response contains the guitars
    data = response.json()
    assert "guitars" in data
    
    # Assert the specific guitars are in the response
    guitars = data["guitars"]
    assert "Fender Strat 62" in guitars
    assert "Gibson Flying V 94" in guitars
    assert "Gibson ES 135" in guitars
    assert "Fender Telecaster Highway 1" in guitars
