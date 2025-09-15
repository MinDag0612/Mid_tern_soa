from passlib.context import CryptContext

context_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

print(context_pwd.hash("pass02"))