# 추천 모델 함수
def recommend_clubs(selected_club, final_similarity, data, top_n=3):
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

