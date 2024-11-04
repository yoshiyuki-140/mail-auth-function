import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app
from models import User

############### テスト用のダミーデータを作成 ###############

load_dotenv()

db_user = os.getenv("POSTGRES_USER")  # postgreSQLのユーザー名
db_pass = os.getenv("POSTGRES_PASSWORD")  # postgreSQLのパスワード
db_name = os.getenv(
    "POSTGRES_DEV_DB", "test_db"
)  # postgreSQLのテストコード動作時のDB名
db_name = "test_db"

if not db_user or not db_pass:
    print(
        "Warning: データベースユーザーまたはパスワードが見つかりません。'.env' ファイルを確認してください。"
    )

# PostgreSQL用のテストデータベースURL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{db_user}:{db_pass}@localhost:5432/{db_name}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# テスト用データベースの準備
@pytest.fixture(scope="session")
def db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")
    db = TestingSessionLocal()
    try:
        db.add_all(
            [
                # User(id=1, name="test1", email="user1@example.com", password="string1"),
                # User(id=2, name="test2", email="user2@example.com", password="string2"),
                User(name="test1", email="user1@example.com", password="string1"),
                User(name="test2", email="user2@example.com", password="string2"),
            ]
        )
        db.commit()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


# アプリの依存関係のオーバーライド
@pytest.fixture(scope="session")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client


############### ここからテスト ###############


def test_create_user(client):
    """create_user関数のテスト"""
    response = client.post(
        "/user",
        json={"name": "string", "email": "test@example.com", "password": "string"},
    )
    assert response.status_code == 200
    assert response.json() == {"code": "0", "Message": "Success"}


def test_get_user(client):
    """get_user関数のテスト"""
    response = client.get("/user/1")
    assert response.status_code == 200
    assert response.json() == {
        "name": "test1",
        "email": "user1@example.com",
        "password": "string1",
    }

    response = client.get("/user/2")
    assert response.status_code == 200
    assert response.json() == {
        "name": "test2",
        "email": "user2@example.com",
        "password": "string2",
    }


def test_put_user(client):
    """put_user関数のテスト"""
    response = client.put(
        "/user/1",
        json={
            "name": "modified_test1",
            "email": "modified_user1@example.com",
            "password": "modified_string1",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "modified_test1",
        "email": "modified_user1@example.com",
        "password": "modified_string1",
    }


def test_delete_user(client):
    """delete_user関数のテスト"""
    response = client.delete("/user/1")
    assert response.status_code == 200
    assert response.json() == {"StatusMessage": "Success Delete Params"}


############### temporary_usersテーブルのためのテスト ###############


# @pytest.mark.skip(reason="調査のためスキップ")
def test_add_temporary_user_info(client):
    """temporary_usersテーブルに新しいユーザー情報とトークンを生成する

    Args:
        client (_type_): _description_
    """
    request_body = {"name": "string", "email": "user@example.com", "password": "string"}

    response = client.post("/temporary_user/", json=request_body)

    # DBからデータを取得
    db = TestingSessionLocal()
    user_id = 1
    q = text("select name,email,password from temporary_users where id = :id")
    params = {"id": user_id}
    try:
        result = db.execute(q, params)
        row = result.fetchone()
        if row:
            print("DEBUG : row is exist")
            name, email, password = row  # 取得したデータを変数に代入
        else:
            print("Error: User not found in database")
            assert False, "User data not found in database."
    except SQLAlchemyError as e:
        print("Error:", e)
    finally:
        db.close()

    # 検証
    ## check status code
    assert response.status_code == 200
    ## Is response body
    assert response.json() == {"Success": "temporary user was stored"}
    ## DBにきちんとデータが作られたか否かを調べる
    assert request_body == {"name": name, "email": email, "password": password}


# @pytest.mark.skip(reason="調査のためスキップ")
def test_auth_temporary_user(client):
    """テスト作成時では生成されるトークンは固定化している。
    そのため、本番ではスキップするか、別の方法でtemporary_usersに登録される
    tokenの固定化を行うこと。

    Args:
        client (_type_): _description_
    """

    # セッション情報を登録
    db = TestingSessionLocal()

    # これから登録するデータが、まだusersテーブルに登録されていないことを確認する.
    q = text("select name,email,password from users where id = :id")
    params = {"id": 1}

    try:
        result = db.execute(q, params)
        count_of_rows = len(result.fetchall())
        assert count_of_rows == 0, "Error:そのユーザーはすでに本登録が完了しています。"
    except SQLAlchemyError as e:
        print("Error:", e)
    finally:
        db.close()

    # 当該エントリポイントにリクエスト実行
    request_body = {"email": "user@example.com", "token": 999999}
    response = client.post("/temporary_user/token_auth/", json=request_body)

    # temporary_usersテーブルから当該ユーザー情報が削除されたことを確認する
    q = text("select name,email,password from temporary_users where id = :id")
    params = {"id": 1}
    try:
        result = db.execute(q, params)
        count_of_rows = len(result.fetchall())
        assert (
            count_of_rows == 0
        ), "Error:temporary_usersテーブルから情報が適切に削除されていません。"
    except SQLAlchemyError as e:
        print("Error:", e)
    finally:
        db.close()

    # usersテーブルに情報が登録されたことを確認する
    q = text("select * from users where email = :email")
    params = {"email": request_body["email"]}
    try:
        result = db.execute(q, params)
        count_of_rows = len(result.fetchall())
        assert (
            count_of_rows == 1
        ), "Error:ユーザー情報がusersテーブルに本登録できていません"
    except SQLAlchemyError as e:
        print("Error:", e)
    finally:
        db.close()

    # ステータスコードのチェック
    assert response.status_code == 200
    # レスポンスのボディーのチェック
    assert response.json() == {"code": "0", "Message": "Success"}
