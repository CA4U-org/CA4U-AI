from fastapi import FastAPI, Query
from typing import List
from pydantic import BaseModel


app = FastAPI()

global model

@app.get("/")
#async def root():
def root():
    data = fetcher()
    data = adapter(data)
    data = preprocess(data)
    model = analysis(data)

@app.get("/model-use")
def modelUse(): 
    return model(favorites)