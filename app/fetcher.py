import os
import requests
import base64
import zipfile
import gzip
from io import BytesIO
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from core.ctx import CTX


def club_fetcher():
    club_data = CTX.DB.find_all("CLUB")
    club_df = pd.DataFrame(club_data)
    return club_df

def user_fetcher():
    favorite_data = CTX.DB.find_all("FAVORITE")
    favorite_df = pd.DataFrame(favorite_data)
    return favorite_df


def item_fetcher():

    load_dotenv()
    API_KEY = os.getenv("AMPLITUDE_API_KEY")
    API_SECRET = os.getenv("AMPLITUDE_API_SECRET")

    current_date = datetime.utcnow().strftime("%Y%m%dT%H")

    # API 요청 설정
    EXPORT_URL = "https://amplitude.com/api/2/export"
    params = {"start": "20241118T00", "end": current_date}  # end는 현재 UTC 날짜
    auth_header = base64.b64encode(f"{API_KEY}:{API_SECRET}".encode()).decode()
    headers = {"Authorization": f"Basic {auth_header}"}

    # API 요청
    response = requests.get(EXPORT_URL, params=params, headers=headers)

    # 응답 성공 처리
    if response.status_code == 200 and response.headers.get('Content-Type') == "application/zip":
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            all_data = [
                json.loads(line)
                for file_name in z.namelist()
                for line in gzip.GzipFile(fileobj=BytesIO(z.open(file_name).read())).read().decode('utf-8').strip().split("\n")]

        click_data = pd.DataFrame(all_data)
        return click_data