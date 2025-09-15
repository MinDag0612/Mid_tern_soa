from fastapi import FastAPI
from core.connDB import connDB
from api.account import account_router
from api.tuition import tuition_rounter

app = FastAPI()

app.include_router(account_router, prefix="/accounts", tags=["account"])
app.include_router(tuition_rounter, prefix="/tuition", tags=["tuition"])

@app.get("/")
def test_main():
    return "Fast API success"
