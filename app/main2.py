from fastapi import FastAPI
from typing import List
import pandas as pd
import numpy as np
from fetcher import fetcher
from adapter import adapter
from preprocess import preprocess
from analysis import analysis
from recommend_clubs import recommend_clubs

app = FastAPI()


model_data = None

# 루트 엔드포인트
@app.get("/")
def root():
    global model_data
    df = fetcher()
    adapted_data = adapter(df)
    final_similarity, data = analysis(preprocess(adapted_data))
    model_data = final_similarity, data  # 모델에 결과 저장

## 추천 시스템 엔드포인트
@app.get("/model-use")
def model_use():
    global model_data
    selected_club = 'Club A'  # 일단 고정된 값으로 'Club A' 지정
    final_similarity, data = model_data
    recommended_clubs = recommend_clubs(selected_club, final_similarity, data)
    return {"추천 동아리": recommended_clubs}

