from fastapi import FastAPI
from typing import List
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fetcher import fetcher
from adapter import adapter
from preprocess import preprocess
from analysis import analysis
from recommend_clubs import recommend_clubs

app = FastAPI()


recommend_model = None


@app.get("/clubs/recommend/create")
def create_recommend_model():
    global recommend_model
    if recommend_model is None:  
        df = fetcher()
        adapted_data = adapter(df)
        final_similarity, data = analysis(preprocess(adapted_data))
        recommend_model = final_similarity, data
        return {"message": "추천 모델이 성공적으로 생성되었습니다."}
    else:
        return {"message": "추천 모델이 이미 생성되어 있습니다."}

# 추천 시스템 엔드포인트
@app.get("/clubs/recommend")
def get_recommendations():
    global recommend_model
    favorites = '피카통' 
    final_similarity, data = recommend_model
    recommended_clubs = recommend_clubs(favorites, final_similarity, data)
    return {"recommended_club": recommended_clubs}
