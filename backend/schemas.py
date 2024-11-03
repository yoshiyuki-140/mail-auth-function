# from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserInformation(BaseModel):
    """ユーザー情報の定義

    Args:
        BaseModel (_type_): _description_
    """

    name: str
    email: EmailStr
    password: str


class ReadUserInfo(BaseModel):
    """ユーザー情報をAPIで呼ぶときのデータ構造

    Args:
        BaseModel (_type_): _description_
    """

    name: str
    email: EmailStr
    password: str


class TemporaryUserInformation(BaseModel):
    """ユーザー情報一時保存のためのスキーマ

    Args:
        BaseModel (_type_): _description_
    """

    name: str
    email: EmailStr
    password: str


class AuthTemporaryUserInformation(BaseModel):
    """メールに送信したトークンで認証を行うときのリクエストボディー

    Args:
        BaseModel (_type_): _description_
    """

    email: EmailStr
    token: int
