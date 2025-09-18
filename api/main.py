from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.account import account_router
from api.otp import otp_router
from api.payment import payment_router
from api.tuition import tuition_router

app = FastAPI()

frontend_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account_router, prefix="/accounts", tags=["account"])
app.include_router(tuition_router, prefix="/tuition", tags=["tuition"])
app.include_router(otp_router, prefix="/otp", tags=["otp"])
app.include_router(payment_router, prefix="/payment", tags=["payment"])


@app.get("/")
def test_main():
    return "Fast API success"
