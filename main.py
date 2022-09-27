# main.py
# 실행은 uvicorn main:app --reload --port 8000 --host <컴퓨터 아이피>
# 라이브러리 import
# StreamingResponse를 가져와야함
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

# cv2 모듈 import
from cvtest import get_stream_video

# FastAPI객체 생성
app = FastAPI()

# openCV에서 이미지 불러오는 함수
def video_streaming():
    return get_stream_video()

# 스트리밍 경로를 /video 경로로 설정.
@app.get("/video")
def main():
    # StringResponse함수를 return하고,
    # 인자로 OpenCV에서 가져온 "바이트"이미지와 type을 명시
    return StreamingResponse(video_streaming(), media_type="multipart/x-mixed-replace; boundary=frame")