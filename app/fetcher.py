import pandas as pd

# 동아리/학회 정보 데이터 업로드 함수
def club_fetcher():
    df = pd.read_excel("dataSource/CA4Udata.xlsx")
    return df

# 사용자 즐겨찾기 더미 데이터 업로드 함수
def user_fetcher():
    user_favorites = pd.read_excel("dataSource/user_favorites_dummy.xlsx")
    return user_favorites