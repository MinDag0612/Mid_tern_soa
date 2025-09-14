from fastapi import FastAPI
from core.connDB import connDB
from api.account import account_router

app = FastAPI()

app.include_router(account_router, prefix="/accounts", tags=["account"])

@app.get("/")
def test_main():
    return "Fast API success"
