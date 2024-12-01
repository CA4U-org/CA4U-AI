def update_content_recommend_model():
    from main import initialize_content_model
    global content_recommend_model
    content_recommend_model = initialize_content_model()
    print("콘텐츠 추천 모델이 갱신되었습니다.")

def update_user_recommend_model():
    from main import initialize_user_model
    global user_recommend_model
    user_recommend_model = initialize_user_model()
    print("사용자 추천 모델이 갱신되었습니다.")

def update_item_recommend_model():
    from main import initialize_item_model
    global item_recommend_model
    item_recommend_model = initialize_item_model()
    print("아이템 추천 모델이 갱신되었습니다.")

