from fastapi import FastAPI, Query
from typing import List
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
#async def root():
def root():
    return {"message" : "woong world!@@@@@@@@@@@@@@@@@"}

@app.get("/home")
def home():
    return {"message" : "home"}

@app.get("/ai/service")
def recommend_ai(number: int = Query(..., description="Input a number (1, 5, 7)")):
    if number == 1:
        return {"message": 2}
    elif number == 5:
        return {"message": 6}
    elif number == 7:
        return {"message": 7}
    else:
        return {"error": "Invalid number, please provide 1, 5, or 7"}

class NumberListInput(BaseModel):
    numbers: List[int]

@app.post("/ai/service")
def recommend_ai_post(numbers_input: NumberListInput):
    numbers = numbers_input.numbers
    result = {}

    if 1 in numbers and 2 in numbers and 3 in numbers:
        result['result'] = [11, 13, 15]
    else:
        return {"message": "1, 2, 3으로 다시 시도해주세요."}

    return result