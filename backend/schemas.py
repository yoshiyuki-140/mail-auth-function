# from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserInformation(BaseModel):
    """
    呼び出し時
    - ユーザー作成時
    """

    name: str
    email: EmailStr
    password: str


class ReadUserInfo(BaseModel):
    name: str
    email: EmailStr
    password: str
