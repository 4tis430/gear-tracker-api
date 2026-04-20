from fastapi.testclient import TestClient
from main import app


def test_get_guitars():
    """
    Test that the /guitars endpoint returns the correct structure and data types.
    """
    client = TestClient(app)
    response = client.get("/guitars")
    
    # Assert status code is 200
    assert response.status_code == 200
    
    # Assert response is a dictionary containing 'guitars' key
    data = response.json()
    assert isinstance(data, dict)
    assert "guitars" in data
    
    # Assert deployment_timestamp is present and is a string
    assert "deployment_timestamp" in data
    assert isinstance(data["deployment_timestamp"], str)
    
    # Assert the value of 'guitars' is a list
    guitars = data["guitars"]
    assert isinstance(guitars, list)
    assert len(guitars) > 0
    
    # Assert each item in the list has the required keys with correct data types
    for guitar in guitars:
        assert isinstance(guitar, dict)
        assert "brand" in guitar
        assert "model" in guitar
        assert "year" in guitar
        
        # Verify data types
        assert isinstance(guitar["brand"], str)
        assert isinstance(guitar["model"], str)
        assert isinstance(guitar["year"], int)
