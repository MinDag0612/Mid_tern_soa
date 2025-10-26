from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.account import account_router
from api.otp import otp_router
from api.payment import payment_router
from api.tuition import tuition_router
from api.mailler import mailler_router
from services.jwt_service import jwt_services

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

jwt_services = jwt_services()

app.include_router(account_router, prefix="/accounts", tags=["account"])
app.include_router(tuition_router, prefix="/tuition", tags=["tuition"], dependencies=[Depends(jwt_services.get_current_user)])
app.include_router(otp_router, prefix="/otp", tags=["otp"], dependencies=[Depends(jwt_services.get_current_user)])
app.include_router(payment_router, prefix="/payment", tags=["payment"], dependencies=[Depends(jwt_services.get_current_user)])
app.include_router(mailler_router, prefix="/mailler", tags=["mailler"], dependencies=[Depends(jwt_services.get_current_user)])


@app.get("/")
def test_main():
    return "Fast API success"
