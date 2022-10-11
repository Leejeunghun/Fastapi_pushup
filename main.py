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

#템플릿 활용

from fastapi.templating import Jinja2Templates #템플릿 추가
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi import Request

#데이터 베이스 가져오기
from db import session
from model import *
from typing import List


app.mount("/templates", StaticFiles(directory="templates"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/users", response_class=HTMLResponse)# 사용 하지 않는 함수
async def read_users(request: Request):
    print("read_users >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    context = {}
    users = session.query(UserTable).all()
    context['request'] = request
    context['users'] = users
    return templates.TemplateResponse("user.html", context)



# ----------API 정의------------
@app.get("/users/{user_id}")
def read_user(user_id: int):
    user = session.query(UserTable).filter(UserTable.id == user_id).first()
    return user

@app.post("/users")
async def create_user(users: User):
    print("create_user >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # data = await request.json()
    userlist = list(users)

    uname = userlist[1][1]
    uage = userlist[2][1]

    user = UserTable()
    user.NAME = uname
    user.COUNT = uage

    session.add(user)
    session.commit()

    return { 'result_msg': f'{uname} Registered...' }

@app.put("/users")
async def modify_users(users: User):
    print("modify_user >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    userlist = list(users)
    uid = userlist[0][1]
    uname = userlist[1][1]
    ucount = userlist[2][1]

    user: User = session.query(UserTable).filter(UserTable.PK == uid).first()
    user.NAME = uname
    user.COUNT = ucount
    session.commit()

    return { 'result_msg': f"{uname} updated..." }


@app.delete("/users")
async def delete_users(users: User):
    print("delete_user >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    userlist = list(users)
    uid = userlist[0][1]

    user = session.query(UserTable).filter(UserTable.PK == uid).delete()
    session.commit()

    return {'result_msg': f"User deleted..."}



# openCV에서 이미지 불러오는 함수
def video_streaming():
    return get_stream_video()

# 스트리밍 경로를 /video 경로로 설정.
@app.get("/video")
def main():
    # StringResponse함수를 return하고,
    # 인자로 OpenCV에서 가져온 "바이트"이미지와 type을 명시
    return StreamingResponse(video_streaming(), media_type="multipart/x-mixed-replace; boundary=frame")