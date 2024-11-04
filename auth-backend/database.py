import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv

dialect = "postgresql"
driver = "psycopg2"
username = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "psql")
host = "localhost"
port = "5432"
database = os.getenv("POSTGRES_DB", "postgres")

database = "postgres"
url = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(url, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
