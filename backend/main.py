# api routing

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

load_dotenv()  # .envから環境変数に読み出し


app = FastAPI()


# オリジン間リソース共有の設定

origins = [
    # "http://localhost",
    # "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# test entry posint
@app.get("/")
def get():
    return {"HelloWorld": "This is Operation confirmation Entrypoint"}


# CREATE
@app.post("/user")
def create_user(
    body: schemas.UserInformation,
    db: Session = Depends(get_db),
):
    # ユーザー作成
    if crud.create_user(db, body.name, body.email, body.password) == True:
        return {"code": "0", "Message": "Success"}
    else:
        return {"code": "-1", "Message": "Failed"}


# READ
@app.get("/user/{user_id}", response_model=schemas.UserInformation)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """ユーザー情報をDBから取得する関数

    Args:
        user_id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    name, email, password = crud.read_user(db, user_id)
    return {"name": name, "email": email, "password": password}


# UPDATE
@app.put("/user/{user_id}", response_model=schemas.UserInformation)
def put_user(
    user_id: int,
    body: schemas.UserInformation,
    db: Session = Depends(get_db),
):
    """ユーザー情報を更新するためのエントリポイント

    Args:
        user_id (int): _description_
        body (schemas.UserInformation): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    name, email, password = crud.update_user(
        user_id,
        body.name,
        body.email,
        body.password,
        db,
    )
    return {"name": name, "email": email, "password": password}


# DELETE
@app.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """ユーザーを削除するためのエントリポイント

    Args:
        user_id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    crud.delete_user(db, user_id)
    return {"StatusMessage": "Success Delete Params"}


#################### ユーザー情報一時保存テーブルに情報を保存する ####################


@app.post("/temporary_user/")
def add_temporary_user_info(
    body: schemas.TemporaryUserInformation, db: Session = Depends(get_db)
):
    """temporary_usersテーブルに新しいユーザー情報とトークンを作成する

    Args:
        body (schemas.TemporaryUserInformation): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    """
    crud.create_temporary_user(db, body.name, body.email, body.password)
    return {"Success": "temporary user was stored"}


# トークン情報を認証して一時保存テーブルからユーザー情報保存テーブルに情報を保存するエントリポイント
@app.post("/temporary_user/token_auth")
def auth_temporary_user(
    body: schemas.AuthTemporaryUserInformation, db: Session = Depends(get_db)
):
    """リクエストボディーからトークンを取得し、temporary_usersテーブルに登録されたユーザーと同じなら
    usersテーブルにユーザー情報を登録し、サインアップを完了するためのエントリポイント

    Args:
        body (schemas.AuthTemporaryUserInformation): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    """
    result = crud.auth_temporary_user_by_token(db, body.email, body.token)
    if result:
        # 認証に成功した時
        return {"code": "0", "Message": "Success"}
    else:
        # 認証に失敗した時
        return {"code": "-1", "Message": "Failed"}
