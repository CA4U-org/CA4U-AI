from fastapi import FastAPI
from typing import List
from adapter import content_adapter, user_adapter
from preprocess import preprocess
from analysis import analysis
from recommend_clubs import content_recommend_clubs, content_recommend_clubs_n, user_recommend_clubs
import core.boot
from core.ctx import CTX
from fetcher import club_fetcher, user_fetcher

app = FastAPI()  

club_fetcher_df= club_fetcher()
user_fetcher_df= user_fetcher()

print(club_fetcher_df)
print(user_fetcher_df)