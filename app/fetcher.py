import pandas as pd
from core.ctx import CTX

# 동아리/학회 정보 데이터 업로드 함수
def club_fetcher():
    club_data = CTX.DB.find_all("CLUB")
    club_df = pd.DataFrame(club_data)
    return club_df

def user_fetcher():
    favorite_data = CTX.DB.find_all("FAVORITE")
    favorite_df = pd.DataFrame(favorite_data)
    return favorite_df