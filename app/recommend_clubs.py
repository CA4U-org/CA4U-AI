from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from analysis import analysis

# 콘텐츠 필터링 추천 모델
def content_recommend_clubs(selected_id, final_similarity, data, top_n=3):
    idx = data[data['id'] == int(selected_id)].index[0]
    sim_scores = [
        (i, score) for i, score in enumerate(final_similarity[idx]) if i != idx
    ]
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_clubs = [
        {"id": int(data['id'][i[0]]), "name": data['club_nm'][i[0]]}
        for i in sim_scores[:top_n]
    ]
    return top_clubs

# 콘텐츠 필터링 추천 모델(ID 복수 입력 가능)
def content_recommend_clubs_n(selected_ids, final_similarity, data, top_n=3):
    aggregated_scores = {}
    excluded_ids = set(selected_ids)
    
    for selected_id in selected_ids:
        idx = data[data['id'] == int(selected_id)].index[0]
        sim_scores = [
            (i, score) for i, score in enumerate(final_similarity[idx]) if i != idx
        ]
        for i, score in sim_scores:
            aggregated_scores[i] = aggregated_scores.get(i, 0) + score
    

    filtered_scores = {
        i: score for i, score in aggregated_scores.items() 
        if int(data['id'][i]) not in excluded_ids
    }
    
    top_recommended = sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_clubs = [
        {"id": int(data['id'][i]), "name": data['club_nm'][i]}
        for i, _ in top_recommended
    ]
    
    return top_clubs


def user_recommend_clubs(user_id, user_favorites, club_data, click_similarity, top_n=2, click_weight=0.5, favorite_weight=0.5):
    # 즐겨찾기 기반 유사도 
    favorite_similarity, _ = analysis(club_data)
    
    # 사용자 클럽 정보 추출
    user_clubs = user_favorites[user_favorites['user_id'] == user_id]['club_id']
    user_club_data = club_data[club_data['id'].isin(user_clubs)]
    
    # 사용자 간 final 유사도 계산
    user_similarity = {}
    for other_user in user_favorites['user_id'].unique():
        if other_user == user_id:
            continue
        
        # favorite_similarity 
        if user_id in user_favorites['user_id'].values:  
            other_clubs = user_favorites[user_favorites['user_id'] == other_user]['club_id']
            other_club_data = club_data[club_data['id'].isin(other_clubs)]

            favorite_similarities = [
                favorite_similarity[user_club_id - 1, other_club_id - 1]
                for user_club_id in user_club_data['id']
                for other_club_id in other_club_data['id']
            ]
            favorite_sim = np.mean(favorite_similarities) if favorite_similarities else 0
        else:
            favorite_sim = 0  

        # click_similarity 
        if user_id in click_similarity.index:
            click_sim = click_similarity.at[user_id, other_user] if other_user in click_similarity.columns else 0
        else:
            click_sim = 0  

        # 두 유사도의 가중 평균 계산
        total_similarity = (click_weight * click_sim) + (favorite_weight * favorite_sim)

        user_similarity[other_user] = total_similarity

    # 가장 유사한 사용자들 추출
    most_similar_users = sorted(user_similarity.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # 추천 동아리 추출
    recommended_clubs = set()
    for similar_user, _ in most_similar_users:
        similar_user_clubs = user_favorites[user_favorites['user_id'] == similar_user]['club_id']
        recommended_clubs.update(similar_user_clubs)

    recommended_clubs -= set(user_clubs)  # 이미 즐겨찾기한 동아리는 제외

    # 추천 동아리 정보 반환
    top_clubs = [
        {"id": int(row['id']), "name": row['club_nm']}
        for _, row in club_data[club_data['id'].isin(recommended_clubs)].iterrows()
    ]
    return top_clubs