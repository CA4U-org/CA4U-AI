# CA4U-AI
추천시스템 플로우
![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/05e1a22f-2edc-4ba0-8100-67767b4119bd/a968673a-565b-4460-a16d-1c47b9c239aa/image.png)

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

