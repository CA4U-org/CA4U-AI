import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Analysis 함수
def analysis(data):
    
    tfidf_matrix = {}
    for col in data.columns[1:]:
        vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
        tfidf_matrix[col] = vectorizer.fit_transform(data[col])

    cosine_sim = {}
    for col in data.columns[1:]:
        cosine_sim[col] = cosine_similarity(tfidf_matrix[col])

    weights = {
        'id':0,
        'club_nm': 0,
        'category_id':0.5,
        'brief_description': 0.5,
        'recruit_description': 0.5,
        'target_people_description': 0.3,
        'target_cycle_description': 0.1,
        'apply_description': 0.3,
        'act_day_description': 0.3,
        'location_description': 0.1,
        'cost_description': 0.1,
        'spec_description': 0.5
    }

    final_similarity = np.zeros_like(cosine_sim[data.columns[1]])
    for col in data.columns[1:]:
        final_similarity += weights[col] * cosine_sim[col]
    
    return final_similarity, data

def click_analysis(df):
 
    interaction_counts = df.groupby(['user_id', 'club_id']).size().reset_index(name='interaction')
    interaction_counts = interaction_counts[interaction_counts['interaction'] > 0]
    interaction_matrix = interaction_counts.pivot(index='user_id', columns='club_id', values='interaction').fillna(0)
    # 희소 행렬
    interaction_matrix = interaction_matrix.astype(pd.SparseDtype("int", fill_value=0))
    
    # 클릭로그 기반 유사도 계산
    user_similarity_matrix = cosine_similarity(interaction_matrix)
    click_similarity = pd.DataFrame(
        user_similarity_matrix,
        index=interaction_matrix.index,
        columns=interaction_matrix.index)
    
    return click_similarity
