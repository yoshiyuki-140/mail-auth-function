import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from database import Base, get_db
from main import app
from models import User
from dotenv import load_dotenv

############### テスト用のダミーデータを作成 ###############

load_dotenv()

db_user = os.getenv("POSTGRES_USER")  # postgreSQLのユーザー名
db_pass = os.getenv("POSTGRES_PASSWORD")  # postgreSQLのパスワード
db_name = os.getenv("POSTGRES_DB", "test_db")  # postgreSQLのテストコード動作時のDB名

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
    assert response.json() == {"Success": "user was created"}


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
