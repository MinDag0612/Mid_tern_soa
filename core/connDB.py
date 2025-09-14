from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os

class connDB:
    def __init__(self):
        server_name = os.getenv("DB_SERVER", "LAPTOP-MRCSJP4A\\SQLEXPRESS01")
        db_name     = os.getenv("DB_NAME", "tuition_system")
        driver      = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
        trusted     = os.getenv("DB_TRUSTED", "yes")

        DATABASE_URL = (
            f"mssql+pyodbc://@{server_name}/{db_name}"
            f"?driver={driver.replace(' ', '+')}&trusted_connection={trusted}"
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
