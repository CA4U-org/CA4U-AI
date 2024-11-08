from fastapi import FastAPI
from typing import List
from app.fetcher import club_fetcher
from app.fetcher import user_fetcher
from app.adapter import adapter
from app.preprocess import preprocess
from app.analysis import analysis
from app.recommend_clubs import content_recommend_clubs
from app.recommend_clubs import content_recommend_clubs_n
from app.recommend_clubs import user_recommend_clubs

app = FastAPI()


content_recommend_model = None
user_recommend_model = None


# content-recommend 모델 생성
@app.get("/clubs/content/recommend/create")
def create_recommend_model():
    global content_recommend_model
    if content_recommend_model is None:  
        fetcher_df = club_fetcher()
        adapted_df = adapter(fetcher_df)
        preprocess_df = preprocess(adapted_df)
        final_similarity, final_data = analysis(preprocess_df)
        content_recommend_model = final_similarity, final_data
        return {"message": "추천 모델이 성공적으로 생성되었습니다."}
    else:
        return {"message": "추천 모델이 이미 생성되어 있습니다."}


# content-recommend 시스템 (경로 매개변수 사용)
@app.get("/clubs/content/recommend/{clubID}")
def get_recommendations(clubID: int):
    global content_recommend_model
    final_similarity, final_data = content_recommend_model
    content_recommended_clubs = content_recommend_clubs(clubID, final_similarity, final_data)
    return {"recommended_club": content_recommended_clubs}

# 여러 clubID를 쉼표로 구분하여 입력받는 content-recommend 시스템
@app.get("/clubs/content/recommend/n/{clubIDs}")
def get_recommendations(clubIDs: str, top_n: int = 3):
    global content_recommend_model
    final_similarity, final_data = content_recommend_model
    selected_ids = [int(id.strip()) for id in clubIDs.split(",")] # clubIDs를 쉼표로 구분하여 리스트로 변환
    recommended_clubs = content_recommend_clubs_n(selected_ids, final_similarity, final_data, top_n=top_n)
    return {"recommended_clubs": recommended_clubs}

# user-recommend 모델 생성
@app.get("/clubs/user/recommend/create")
def create_recommend_model():
    global user_recommend_model
    if user_recommend_model is None:
        fetcher_df = club_fetcher()
        adapted_df = adapter(fetcher_df)
        club_df = preprocess(adapted_df)
        user_favorites = user_fetcher()
        user_recommend_model = (club_df, user_favorites)
        return {"message": "추천 모델이 성공적으로 생성되었습니다."}
    else:
        return {"message": "추천 모델이 이미 생성되어 있습니다."}


# user-recommend 시스템 (경로 매개변수 사용)
@app.get("/clubs/user/recommend/{userID}")
def get_recommendations(userID: int):
    global user_recommend_model
    club_df, user_favorites = user_recommend_model
    user_recommended_clubs = user_recommend_clubs(userID, user_favorites, club_df)
    return {"recommended_club": user_recommended_clubs}