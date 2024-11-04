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


model_data = None


@app.get("/")
def root():
    global model_data
    df = fetcher()
    adapted_data = adapter(df)
    final_similarity, data = analysis(preprocess(adapted_data))
    model_data = final_similarity, data  

@app.get("/model-use")
def model_use():
    global model_data
    favorites = '피카통' 
    final_similarity, data = model_data
    recommended_clubs = recommend_clubs(favorites, final_similarity, data)
    return {"recommended_club": recommended_clubs}

