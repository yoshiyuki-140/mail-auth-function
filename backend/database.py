from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

dialect = "postgresql"
driver = "psycopg2"
username = "postgres"
password = "psql"
host = "localhost"
port = "5432"
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
