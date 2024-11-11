from dotenv import load_dotenv
import os

load_dotenv()  

PROFILE = os.getenv("PROFILE")
DB_HOST = os.getenv("DB_HOST")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD") 

# PROFILE이 production일 경우, 필수 환경 변수들을 확인
if PROFILE == "production":
    if not DB_HOST:
        raise ValueError("DB_HOST 환경 변수가 설정되지 않았습니다.")
    if not DB_USERNAME:
        raise ValueError("DB_USERNAME 환경 변수가 설정되지 않았습니다.")
    if not DB_PASSWORD:
        raise ValueError("DB_PASSWORD 환경 변수가 설정되지 않았습니다.")