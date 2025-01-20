# CA4U-AI
- 추천시스템 플로우
![추천시스템 플로우](recommendation%20system%20flow.png)

- 추천시스템 기능
  
  1. 콘텐츠 기반 필터링 (Content-Based Filtering)
  2. 사용자 협업 필터링 (User-Based Collaborative Filtering)

- 성능평가 \
  \
    app 파일 > performance_test.py 가중치 조정 후, 성능지표 확인 가능 

## Required

Python 3.11.0

## How to run in python 3.11.0

python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
cd app 
uvicorn main:app --reload

## 도커 빌드 방법
docker build -t ca4u-ai-app .
docker run -d -p 8000:80 ca4u-ai-app

