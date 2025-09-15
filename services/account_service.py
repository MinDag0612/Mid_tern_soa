from passlib.context import CryptContext
from repositories.account_repo import AccountRepository
from schemas.account_schema import Infor

class AccountService:
    def __init__(self, repo: AccountRepository):
        self.repo = repo
        self.context_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def login(self, user_name: str, password: str):
        account = self.repo.get_account_by_username(user_name)
        if not account:
            return {"message": "Invalid username or password"}

        if not self.context_pwd.verify(password, account["password"]):
            return {"message": "Invalid username or password"}

        customer = self.repo.get_customer_infor(account["id"])
        if not customer:
            return {"message": "Cannot find infor !!"}
        return Infor(**customer).model_dump()
