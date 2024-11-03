# Analysis ÇÔ¼ö
def analysis(data):
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    tfidf_matrix = {}
    for col in data.columns[1:]:
        vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
        tfidf_matrix[col] = vectorizer.fit_transform(data[col])

    cosine_sim = {}
    for col in data.columns[1:]:
        cosine_sim[col] = cosine_similarity(tfidf_matrix[col])

    weights = {
        'clubNm': 0,
        'briefDescription': 0.5,
        'recruitDescription': 0.5,
        'targetPeopleDescription': 0.3,
        'targetCycleDescription': 0.1,
        'applyDescription': 0.3,
        'actDayDescription': 0.3,
        'locationDescription': 0.1,
        'costDescription': 0.1,
        'specDescription': 0.3
    }

    final_similarity = np.zeros_like(cosine_sim[data.columns[1]])
    for col in data.columns[1:]:
        final_similarity += weights[col] * cosine_sim[col]
    
    return final_similarity, data

