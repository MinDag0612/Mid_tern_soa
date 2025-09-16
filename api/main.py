from fastapi import FastAPI
from core.connDB import connDB
from api.account import account_router
from api.tuition import tuition_router
from api.otp import otp_router
from api.payment import payment_router

app = FastAPI()

app.include_router(account_router, prefix="/accounts", tags=["account"])
app.include_router(tuition_router, prefix="/tuition", tags=["tuition"])
app.include_router(otp_router, prefix="/otp", tags=["otp"])
app.include_router(payment_router, prefix="/payment", tags=["payment"])


@app.get("/")
def test_main():
    return "Fast API success"
