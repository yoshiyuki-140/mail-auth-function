# from typing import List, Optional
from pydantic import BaseModel


class UserInformation(BaseModel):
    """
    呼び出し時
    - ユーザー作成時
    """

    name: str
    password: str


class ReadUserInfo(BaseModel):
    password: str
