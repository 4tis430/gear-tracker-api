from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

# Global variable to track when the application started
START_TIME = datetime.now()

@app.get("/guitars")
def get_guitars():
    """
    Returns a list of guitars in the collection.
    """
    guitars = [
        {"brand": "Fender", "model": "Stratocaster 62 Japan", "year": 1999},
        {"brand": "Gibson", "model": "Flying V", "year": 1994},
        {"brand": "Gibson", "model": "ES 135", "year": 1998},
        {"brand": "Fender", "model": "Telecaster Highway 1", "year": 2005},
        {"brand": "Gibson", "model": "J-45", "year": 2023}
    ]
    return {
        "guitars": guitars,
        "deployment_timestamp": START_TIME.isoformat()
    }
