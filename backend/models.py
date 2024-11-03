from sqlalchemy import Column, Integer, String, CHAR

from database import Base


class User(Base):
    """Userテーブルのモデルクラス

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255))

    email = Column(String(255))

    password = Column(String(255))


class TemporaryUser(Base):
    """temporary_usersテーブルのモデルクラス

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255))

    email = Column(String(255))

    password = Column(String(255))

    token = Column(CHAR(6))
