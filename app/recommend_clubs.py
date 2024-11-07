# 콘텐츠 필터링 추천 모델
def content_recommend_clubs(selected_club, final_similarity, data, top_n=3):
    idx = data[data['clubNm'] == selected_club].index[0]
    sim_scores = list(enumerate(final_similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [x for x in sim_scores if x[0] != idx]  # 선택한 단체 제외
     # 추천 동아리 ID와 이름 포함
    top_clubs = [
        {"id": int(data['ID'][i[0]]), "name": data['clubNm'][i[0]]}
        for i in sim_scores[:top_n]
    ]
    return top_clubs


# 사용자 협업 필터링 추천 모델
def user_recommend_clubs(user_id, user_favorites, club_data, top_n=2):
    import numpy as np
    from analysis import analysis

  
    user_clubs = user_favorites[user_favorites['userID'] == user_id]['clubID']
    user_club_data = club_data[club_data['ID'].isin(user_clubs)]


    final_similarity, _ = analysis(club_data)  # 유사도 행렬만 추출

    # 사용자 간 유사도 계산
    user_similarity = {}
    for other_user in user_favorites['userID'].unique():
        if other_user == user_id:
            continue
        other_clubs = user_favorites[user_favorites['userID'] == other_user]['clubID']
        other_club_data = club_data[club_data['ID'].isin(other_clubs)]

        similarities = []
        for user_club_id in user_club_data['ID']:
            for other_club_id in other_club_data['ID']:
                similarities.append(final_similarity[user_club_id - 1, other_club_id - 1])  # ID를 인덱스로 매핑
        user_similarity[other_user] = np.mean(similarities) if similarities else 0

   
    most_similar_users = sorted(user_similarity.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # 추천 동아리 추출
    recommended_clubs = set()
    for similar_user, _ in most_similar_users:
        similar_user_clubs = user_favorites[user_favorites['userID'] == similar_user]['clubID']
        recommended_clubs.update(similar_user_clubs)

    recommended_clubs -= set(user_clubs)  # 대상 사용자가 이미 즐겨찾기한 동아리는 제외

    top_clubs = [
        {"id": int(row['ID']), "name": row['clubNm']}
        for _, row in club_data[club_data['ID'].isin(recommended_clubs)].iterrows()
    ]
    return top_clubs

