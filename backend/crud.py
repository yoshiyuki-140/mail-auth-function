from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


# CREATE
def create_user(db: Session, name: str, email: str, password: str):
    """ユーザー作成を行う関数"""
    q = text(
        "insert into users (name,email,password) values (:name, :email, :password)"
    )
    params = {
        "name": name,
        "email": email,
        "password": password,
    }
    try:
        result = db.execute(q, params)
        db.commit()
        return result
    except SQLAlchemyError as e:
        db.rollback()
        print("Error occurred:", e)
        return None


# READ
def read_user(db: Session, user_id: int):
    """ユーザー情報を返す関数

    Args:
        db (Session): _description_
        user_id (int): _description_

    Returns:
        _type_: ユーザー名、Eメール、パスワードの情報が返却される
    """
    q = text("select name,email,password from users where id = :id")
    params = {"id": user_id}
    try:
        result = db.execute(q, params)
        row = result.fetchone()
        if row:  # rowが存在すればネスト内を実行
            name = row[0]
            email = row[1]
            password = row[2]
            return name, email, password
        else:
            print("Error : Can't Read Db Error occurred!")
            return None
    except SQLAlchemyError as e:
        db.rollback()
        print("Error : Can't Read Db Error occurred : ", e)
        return None


# UPDATE
def update_user(
    user_id: int,
    name: str,
    email: str,
    password: str,
    db: Session,
):
    """ユーザー情報を更新する関数

    Args:
        user_id (int): _description_
        name (str): _description_
        email (str): _description_
        password (str): _description_
        db (Session): _description_

    Returns:
        _type_: ユーザー名,Eメール,パスワードが返却される
    """
    q = text(
        "update users set name = :name, password = :password, email = :email where id = :user_id"
    )
    params = {
        "name": name,
        "email": email,
        "password": password,
        "user_id": user_id,
    }
    try:
        db.execute(q, params)
        db.commit()
        return name, email, password
    except SQLAlchemyError as e:
        db.rollback()
        print("Error occured:", e)
        return None


# DELETE
def delete_user(db: Session, user_id: int):
    """ユーザーを消す関数

    Args:
        db (Session): _description_
        user_id (int): _description_

    Returns:
        _type_: 消したユーザーの数が返却される。 1->正常,0->異常
    """
    q = text("delete from users where id = :id ")
    params = {"id": user_id}
    try:
        result = db.execute(q, params)
        db.commit()

        # 消された要素の数を表示
        print(f"Deleted {result.rowcount}")
        return result.rowcount
    except SQLAlchemyError as e:
        db.rollback()
        print("Error occured:", e)
        return None
