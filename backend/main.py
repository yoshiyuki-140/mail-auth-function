# api routing
import json
import os
from os.path import dirname, join

import crud
import schemas
import uvicorn
from database import SessionLocal, engine
from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()  # .envから環境変数に読み出し


app = FastAPI()


# オリジン間リソース共有の設定

origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
    # "http://192.168.3.2",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    crud.create_user(db, body.name, body.password)
    return {"Success": "user was created"}


# READ
@app.get("/user/{user_id}", response_model=schemas.UserInformation)
def get_user(user_id: int, db: Session = Depends(get_db)):
    name, password = crud.read_user(db, user_id)
    return {"name": name, "password": password}


# UPDATE
@app.put("/user/{user_id}", response_model=schemas.UserInformation)
def put_user(
    user_id: int,
    body: schemas.UserInformation,
    db: Session = Depends(get_db),
):
    name, password = crud.update_user(
        user_id,
        body.name,
        body.password,
        db,
    )
    return {"name": name, "password": password}


# DELETE
@app.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
    return {"StatusMessage": "Success Delete Params"}
