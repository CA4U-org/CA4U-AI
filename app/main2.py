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

# ��Ʈ ��������Ʈ
@app.get("/")
def root():
    global model_data
    df = fetcher()
    adapted_data = adapter(df)
    final_similarity, data = analysis(preprocess(adapted_data))
    model_data = final_similarity, data  # �𵨿� ��� ����

## ��õ �ý��� ��������Ʈ
@app.get("/model-use")
def model_use():
    global model_data
    selected_club = 'Club A'  # �ϴ� ������ ������ 'Club A' ����
    final_similarity, data = model_data
    recommended_clubs = recommend_clubs(selected_club, final_similarity, data)
    return {"��õ ���Ƹ�": recommended_clubs}

