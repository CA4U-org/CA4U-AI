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

def item_analysis(df):
    #유저-동아리 상호작용 행렬 생성
    interaction_matrix = pd.crosstab(index=df['amplitude_id'], columns=df['club_id'])
    return interaction_matrix