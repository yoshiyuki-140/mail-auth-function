# api routing
import json
import os
from os.path import dirname, join

import uvicorn
from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, engine, get_db

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
    crud.create_user(db, body.name, body.email, body.password)
    return {"Success": "user was created"}


# READ
@app.get("/user/{user_id}", response_model=schemas.UserInformation)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """ユーザー情報をDBに登録するためのエントリポイント

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
