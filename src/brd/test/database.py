import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = os.getenv("DATABASE_URL")
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Qwerty12@localhost:5432/brd"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Qwerty12@localhost:5432/brd"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
