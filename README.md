# CA4U-AI
CA4U프로젝트 AI

## Required

Python 3.11.0

## How to run in python 3.11.0

python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
cd app 
uvicorn main:app --reload

## 도커 빌드 방법
//이미지 생성
docker build -t ca4u-ai-app .

//실행
docker run -d -p 8000:80 ca4u-ai-app

//실행중인 컨테이너 확인
docker ps -a

// HTTPie 설치 (Desktop 용으로)