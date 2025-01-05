from fastapi import FastAPI
from typing import List
from adapter import content_adapter, user_adapter, item_adapter
from preprocess import preprocess, item_preprocess
from analysis import analysis, item_analysis
from recommend_clubs import content_recommend_clubs, content_recommend_clubs_n, user_recommend_clubs, item_recommend_clubs
import core.boot
from core.ctx import CTX
from fetcher import club_fetcher, user_fetcher, item_fetcher

app = FastAPI()  
  
content_recommend_model = None
user_recommend_model = None
item_recommend_model = None

def initialize_content_model():
    fetcher_df = club_fetcher()
    adapted_df = content_adapter(fetcher_df)
    preprocess_df = preprocess(adapted_df)
    final_similarity, final_data = analysis(preprocess_df) 
    return final_similarity, final_data

def initialize_user_model():
    club_df = preprocess(content_adapter(club_fetcher()))
    user_favorites = user_adapter(user_fetcher())
    return club_df, user_favorites

def initialize_item_model():
    fetcher_df = item_fetcher()
    adapted_df = item_adapter(fetcher_df)
    preprocess_df = item_preprocess(adapted_df)
    interaction_matrix = item_analysis(preprocess_df) 
    club_data = club_fetcher()
    return interaction_matrix,club_data


# content-recommend 시스템 (경로 매개변수 사용)
@app.get("/clubs/content/recommend/{clubID}")
def get_recommendations(clubID: int):
    global content_recommend_model
    if content_recommend_model is None:
        content_recommend_model = initialize_content_model()
    final_similarity, final_data = content_recommend_model
    return {"recommended_club": content_recommend_clubs(clubID, final_similarity, final_data)}

# content-recommend 시스템 (복수의 clubID 쉼표로 구분)
@app.get("/clubs/content/recommend/n/{clubIDs}")
def get_recommendations(clubIDs: str, top_n: int = 3):
    global content_recommend_model
    if content_recommend_model is None:
        content_recommend_model = initialize_content_model()
    final_similarity, final_data = content_recommend_model
    selected_ids = [int(id.strip()) for id in clubIDs.split(",")] # clubIDs를 쉼표로 구분하여 리스트로 변환
    return {"recommended_clubs": content_recommend_clubs_n(selected_ids, final_similarity, final_data, top_n=top_n)}

# user-recommend 시스템 (경로 매개변수 사용)
@app.get("/clubs/user/recommend/{userID}")
def get_recommendations(userID: int):
    global user_recommend_model
    user_recommend_model = initialize_user_model()
    club_df, user_favorites = user_recommend_model
    if userID in user_favorites['user_id'].unique():
        return {"recommended_club": user_recommend_clubs(userID, user_favorites, club_df)}
    return {"message": "해당 ID는 유사한 사용자를 찾을 수 없습니다."}

# item-recommend 시스템 (경로 매개변수 사용)
@app.get("/clubs/item/recommend/{clubID}")
def get_recommendations(clubID: int):
    global item_recommend_model
    if item_recommend_model is None:
        item_recommend_model = initialize_item_model()
    interaction_matrix,club_data = item_recommend_model
    if str(clubID) in interaction_matrix.columns:
        return {"recommended_club": item_recommend_clubs(interaction_matrix, clubID, club_data)}
    return {"message": "해당 동아리는 함께 둘러본 동아리를 찾을 수 없습니다."}


@app.on_event("startup")
def start_scheduler():
    CTX.scheduler.start()

# FastAPI 앱 종료 시 스케줄러 종료
@app.on_event("shutdown")  
def shutdown_scheduler():
    CTX.scheduler.shutdown(wait=False)
