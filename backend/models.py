from database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    """Userテーブルのモデルクラス

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255))

    password = Column(String(255))
