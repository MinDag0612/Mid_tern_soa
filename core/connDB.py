from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from a local .env file if present
load_dotenv()


class connDB:
    def __init__(self):
        host = os.getenv("DB_HOST", "mysql")
        port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME", "TuitionDB")
        username = os.getenv("DB_USER", "sa")
        password = os.getenv("DB_PASSWORD", "12345")
        charset = os.getenv("DB_CHARSET", "utf8mb4")

        auth_part = username
        if password:
            auth_part = f"{username}:{password}"

        DATABASE_URL = (
            f"mysql+pymysql://{auth_part}@{host}:{port}/{db_name}"
            f"?charset={charset}"
        )

        # Tạo engine (cầu nối DB)
        self.engine = create_engine(DATABASE_URL, echo=True, future=True)

        # Session để thao tác ORM
        self.SessionLocal = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)

        # Base cho model ORM nếu cần
        self.Base = declarative_base()

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
