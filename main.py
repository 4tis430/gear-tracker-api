from fastapi import FastAPI

app = FastAPI()

@app.get("/guitars")
def get_guitars():
    """
    Returns a list of guitars in the collection.
    """
    guitars = [
        "Fender Strat 62",
        "Gibson Flying V 94",
        "Gibson ES 135",
        "Fender Telecaster Highway 1"
    ]
    return {"guitars": guitars}
