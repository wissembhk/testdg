import os
from fastapi import APIRouter, Depends, Request
from models.schemas import AlertInfoSchema
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT
from services.AlertService import create_alert
from services.AlertService import get_today_alert
from services.AlertService import send_alerts
from utils.redis import redis_consumer
import time

router = APIRouter(prefix="/alert")


@router.post("/login")
def user_login(user: dict):
    if user["user"] == os.getenv("login"):
        return signJWT(user["user"])
    return {
        "error": "Wrong login details!"
    }


@router.post('/add')
async def create_alert_router(alert: AlertInfoSchema):
    return await create_alert(alert)


@router.get('/get', dependencies=[Depends(JWTBearer())])
async def get_data_router():
    return await send_alerts(redis_consumer('alert_list'))


@router.get('/get_today_alerts', dependencies=[Depends(JWTBearer())])
async def get_today_alert_router():

    return await get_today_alert()


@router.get('/testh')
async def test(request: Request):
    return time.tzname
