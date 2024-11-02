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

db_user = os.getenv("POSTGRES_USER")
db_pass = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB", "test_db")

print("This is db user name", db_user)
print("This is db user pass", db_pass)

if not db_user or not db_pass:
    print(
        "警告: データベースユーザーまたはパスワードが見つかりません。'.env' ファイルを確認してください。"
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
    response = client.post(
        "/user",
        json={"name": "string", "email": "test@example.com", "password": "string"},
    )
    assert response.status_code == 200
    assert response.json() == {"Success": "user was created"}


def test_get_user(client):
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
