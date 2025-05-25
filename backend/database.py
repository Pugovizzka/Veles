from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Создание таблиц:
if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
