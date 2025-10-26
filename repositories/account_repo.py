from sqlalchemy.orm import Session
from sqlalchemy import text

class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_account_by_username(self, user_name: str):
        query = text("SELECT * FROM account WHERE userName = :user_name")
        return self.db.execute(
            query, {"user_name": user_name}
        ).mappings().first()
        
    def get_pass_by_username(self, user_name: str):
        query = text("SELECT userName, password FROM account WHERE userName = :user_name")
        return self.db.execute(
            query, {"user_name": user_name}
        ).mappings().first()

    def get_customer_infor(self, customer_id: int):
        query = text("SELECT id, fullName, email FROM CustomerInfor WHERE id = :customer_id")
        return self.db.execute(
            query, {"customer_id": customer_id}
        ).mappings().first()

    def get_customer_with_balance(self, customer_id: int):
        query = text(
            "SELECT id, fullName, email, balance FROM CustomerInfor WHERE id = :customer_id"
        )
        return self.db.execute(query, {"customer_id": customer_id}).mappings().first()  

    def lock_customer_for_update(self, customer_id: int):
        query = text(
            "SELECT id, fullName, email, balance FROM CustomerInfor WHERE id = :customer_id FOR UPDATE"
        )
        return self.db.execute(query, {"customer_id": customer_id}).mappings().first()

    def update_customer_balance(self, customer_id: int, balance):
        query = text(
            "UPDATE CustomerInfor SET balance = :balance WHERE id = :customer_id"
        )
        self.db.execute(query, {"balance": balance, "customer_id": customer_id})
