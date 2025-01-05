import pandas as pd
import numpy as np
import os


#### 1. 동아리 데이터

# 프로젝트 루트 기준 상대 경로 설정
base_dir = os.path.dirname(__file__)
club_d_path = os.path.join(base_dir, 'dataSource/CA4U_d.csv')
club_df = pd.read_csv(club_d_path)
club_df = pd.get_dummies(club_df, columns=['Category']).astype(int)
club_df.set_index('ID', inplace=True)
print(club_df)


#### 2. 사용자 데이터 생성
club_names = club_df.index

num_users = 100
np.random.seed(42)
data = np.random.randint(0, 2, size=(num_users, len(club_names)))

# 사용자 df 생성
users = [f'user_{i+1}' for i in range(num_users)]
user_df = pd.DataFrame(data, index=users, columns=club_names)

print(user_df)

# 사용자별로 리스트 생성
user_id_lists = {}

for user in user_df.index:
    favorite_ids = user_df.columns[user_df.loc[user] == 1].tolist()
    user_id_lists[user] = favorite_ids

for user, ids in user_id_lists.items():
    print(ids)
 
    
#### 3. 내적 계산
user_category_matrix = user_df.dot(club_df)

# normalization
user_category_norm = user_category_matrix.div(user_category_matrix.sum(axis=1), axis=0)
print(user_category_norm)


#### 4. 사용자 선호 판단

result = user_category_norm.reset_index().melt(
    id_vars='index',
    var_name='club',
    value_name='score'
)

# 'is_favorite' 열 추가 (score >= 0.2인 경우 TRUE, 아니면 FALSE)
result['is_favorite'] = result['score'] >= 0.2

result.rename(columns={'index': 'user'}, inplace=True)

print(result)

# 사용자별 true값 목록 정리
def get_user_favorites(result_df):
    favorite_clubs = result_df[result_df['is_favorite']]

    user_favorites = favorite_clubs.groupby('user')['club'].apply(list).reset_index()
    user_favorites.rename(columns={'club': 'favorite_clubs'}, inplace=True)

    user_favorites['favorite_clubs'] = user_favorites['favorite_clubs'].apply(
        lambda clubs: [club.replace('Category_', '') for club in clubs]
    )

    return user_favorites

user_favorites = get_user_favorites(result)

print(user_favorites)


#### 5. 알고리즘 설계
content_recommend_model = None

from main import initialize_content_model

def content_recommend_clubs_n(selected_ids, final_similarity, data, top_n=3):
    aggregated_scores = {}
    for selected_id in selected_ids:
        idx = data[data['id'] == int(selected_id)].index[0]
        sim_scores = [
            (i, score) for i, score in enumerate(final_similarity[idx]) if i != idx
        ]
        for i, score in sim_scores:
            aggregated_scores[i] = aggregated_scores.get(i, 0) + score
    top_recommended = sorted(aggregated_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_clubs = [
        data['category_id'][i]
        for i, _ in top_recommended
    ]
    return top_clubs

def get_recommendations(clubIDs: str, top_n: int = 3):
    global content_recommend_model
    if content_recommend_model is None:
        content_recommend_model = initialize_content_model()
    final_similarity, final_data = content_recommend_model
    selected_ids = [int(id.strip()) for id in clubIDs.split(",")] # clubIDs를 쉼표로 구분하여 리스트로 변환
    return {"recommended_clubs": content_recommend_clubs_n(selected_ids, final_similarity, final_data, top_n=top_n)}

# Example
recommendation_result = get_recommendations("2,6,10,15,17")
print(recommendation_result)


#### 6. 성능평가
# user1의 데이터만 필터링
user1_favorites = user_favorites[user_favorites['user'] == 'user_1']
print(user1_favorites)

# 실제 관심사와 예측 관심사 비교
actual_interests = set(user1_favorites['favorite_clubs'].iloc[0])  # 실제 관심사
predicted_interests = set(recommendation_result["recommended_clubs"]) # 예측 관심사

# Accuracy 계산
correct_predictions = actual_interests.intersection(predicted_interests)
accuracy = len(correct_predictions) / len(predicted_interests) if predicted_interests else 0

print(f"Actual Interests: {actual_interests}")
print(f"Predicted Interests: {predicted_interests}")
print(f"Correct Predictions: {correct_predictions}")
print(f"Accuracy: {accuracy:.2f}")