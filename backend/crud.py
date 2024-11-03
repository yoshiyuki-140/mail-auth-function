from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from common_function import create_token


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
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print("Error occurred:", e)
        return False


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


#################### temporary_usersテーブルに関する操作 ####################


# ユーザー情報を一時保存テーブルに保存する
def create_temporary_user(db: Session, name: str, email: str, password: str):
    """ユーザー作成を行う関数"""
    # ここでトークンを作成する
    token = create_token()

    # ユーザー情報一時保存テーブルにユーザー情報を保存する
    q = text(
        "insert into temporary_users (name,email,password,token) values (:name, :email, :password, :token)"
    )
    params = {
        "name": name,
        "email": email,
        "password": password,
        "token": token,
    }
    try:
        result = db.execute(q, params)
        db.commit()
        return result
    except SQLAlchemyError as e:
        db.rollback()
        print("Error occurred:", e)
        return None


# トークン情報を認証して一時保存テーブルからユーザー情報保存テーブルに情報を保存する
# トークンが一致しなければFalseを返す
def auth_temporary_user_by_token(db: Session, email: str, token: int):
    """トークンからemailの情報を

    Args:
        db (Session): _description_
        email (str): _description_
        token (int): _description_

    Returns:
        _type_: _description_
    """
    q = text("select token,id,name,password from temporary_users where email = :email")
    params = {"email": email}
    try:
        result = db.execute(q, params)  # クエリ実行
        row = result.fetchone()  # クエリ実行結果から一行取得する
        print(row)
        if row:
            acquired_token = int(row[0])
            id = row[1]
            name = row[2]
            password = row[3]
            if acquired_token == token:
                # 認証が成功した時の処理
                ## ユーザーをusersに作る
                if create_user(db, name, email, password):
                    ## temporary_usersテーブルからuserデータを削除する
                    if delete_temporary_user(db, user_id=id):
                        return True
                    else:
                        print(
                            "Error:ユーザー情報一時保存テーブルの情報を消せませんでした"
                        )
                        return False
                else:
                    print("Error:ユーザーテーブルにデータを作成することに失敗しました")
                    return False
            else:
                print("Error:認証が失敗しました")
                return False
        else:
            print("DBからtokenが取ってこれませんでした。")
            return False
    except SQLAlchemyError as e:
        print("Error occurred:", e)
        return False


# ここに一時情報保存テーブルからidによりデータを削除する関数を書く
def delete_temporary_user(db: Session, user_id: int):
    """ユーザー情報一時保存テーブルからユーザデータを削除する関数

    Args:
        db (Session): _description_
        user_id (int): _description_

    Returns:
        _type_: _description_
    """
    q = text("delete from temporary_users where id = :id")
    params = {"id": user_id}
    try:
        result = db.execute(q, params)
        db.commit()
        # 消された要素の数を表示
        print(f"Deleted {result.rowcount}")
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print("Error occured:", e)
        return False
