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
    for selected_id in selected_ids:  # 각 선택된 clubID에 대해 유사도 점수 계산 및 합산
        idx = data[data['id'] == int(selected_id)].index[0]
        sim_scores = [
            (i, score) for i, score in enumerate(final_similarity[idx]) if i != idx
        ]
        for i, score in sim_scores:
            aggregated_scores[i] = aggregated_scores.get(i, 0) + score
    top_recommended = sorted(aggregated_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    top_clubs = [
        {"id": int(data['id'][i]), "name": data['club_nm'][i]}
        for i, _ in top_recommended
    ]
    return top_clubs


# 사용자 협업 필터링 추천 모델
def user_recommend_clubs(user_id, user_favorites, club_data, top_n=2):
    
    user_clubs = user_favorites[user_favorites['user_id'] == user_id]['club_id']
    user_club_data = club_data[club_data['id'].isin(user_clubs)]

    final_similarity, _ = analysis(club_data) 

    # 사용자 간 유사도 계산
    user_similarity = {}
    for other_user in user_favorites['user_id'].unique():
        if other_user == user_id:
            continue
        other_clubs = user_favorites[user_favorites['user_id'] == other_user]['club_id']
        other_club_data = club_data[club_data['id'].isin(other_clubs)]

        similarities = [
            final_similarity[user_club_id - 1, other_club_id - 1]
            for user_club_id in user_club_data['id']
            for other_club_id in other_club_data['id']
        ]
        user_similarity[other_user] = np.mean(similarities) if similarities else 0
  
    most_similar_users = sorted(user_similarity.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # 추천 동아리 추출
    recommended_clubs = set()
    for similar_user, _ in most_similar_users:
        similar_user_clubs = user_favorites[user_favorites['user_id'] == similar_user]['club_id']
        recommended_clubs.update(similar_user_clubs)

    recommended_clubs -= set(user_clubs)  # 대상 사용자가 이미 즐겨찾기한 동아리는 제외

    top_clubs = [
        {"id": int(row['id']), "name": row['club_nm']}
        for _, row in club_data[club_data['id'].isin(recommended_clubs)].iterrows()
    ]
    return top_clubs

# 아이템 기반 협업 필터링 추천 모델
def item_recommend_clubs(interaction_matrix, club_id, club_data, top_n=5):

    # 동아리 간 코사인 유사도 계산
    club_similarity = cosine_similarity(interaction_matrix.T)
    club_similarity_df = pd.DataFrame(
        club_similarity, 
        index=interaction_matrix.columns, 
        columns=interaction_matrix.columns)
    
    similar_clubs = club_similarity_df[str(club_id)].sort_values(ascending=False)[1:top_n+1]
    top_recommended = similar_clubs.index.astype(int).tolist()
    
    top_clubs = [
        {"id": int(club_data['id'][i]), "name": club_data['club_nm'][i]}
        for i in club_data[club_data['id'].isin(top_recommended)].index ]
    return top_clubs