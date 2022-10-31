import os
from utils.database import sessionLocal
from utils.prod_connection import sessionLocalProd
from models.models import PlatformAlert
from models.schemas import AddAlertInfoSchema, AlertInfoSchema
from utils.mail_sender import send_mail
from utils.file_generator import generate_xlfile
from sqlalchemy import select, update
from fastapi import HTTPException
from datetime import date
from typing import List
from utils.redis import redis_producer


async def create_alert(alert: AddAlertInfoSchema):
    alertP = PlatformAlert(
        username=alert.username,
        superproduct_ids=alert.superproduct_ids,
        chain_ids=alert.chain_ids,
        last_time_notified=alert.last_time_notified,
        frequency=alert.frequency,
        threshold=alert.threshold,
        kpi=alert.kpi
    )

    with sessionLocal() as session:
        session.add(alertP)
        try:
            session.commit()
            return alert
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail="Duplicated primary key",

            )


async def update_last_time_notified(id: int):
    with sessionLocal() as session:
        session.execute(update(PlatformAlert)
                        .where(PlatformAlert.id == id)
                        .values(last_time_notified=date.today().strftime("%Y-%m-%d")))
        try:
            session.commit()
        except Exception as e:
            return e


async def get_today_alert():
    statement = select(PlatformAlert).filter(
        PlatformAlert.last_time_notified+PlatformAlert.frequency == date.today())
    with sessionLocal() as session:
        try:
            data = session.execute(statement).all()
        except Exception as e:
            return (e)
    redis_producer(data, 'alert_list')
    return data


async def send_alerts(alerts: List[AlertInfoSchema]):

    for alert in alerts:
        with sessionLocalProd() as session:
            try:
                superproduct_ids = "("+str(alert.superproduct_ids)[1:-1]+")"

                chain_ids = "("+str(alert.chain_ids)[1:-1]+")"
                stat = "select stars,review,user_name,created,superproduct_id from product_reviews where superproduct_id IN "+superproduct_ids + \
                       " and chain_id IN "+chain_ids + \
                       " and created between '"+str(alert.last_time_notified)+"' and '"+date.today().strftime("%Y-%m-%d") + \
                       "' and stars<="+str(alert.threshold) + \
                       " order by superproduct_id  limit 100"
                data = session.execute(stat).all()
            except Exception as e:
                return (e)
        if (len(data) != 0):
            filename = str(os.getenv("DIRECTORY")) + \
                str(alert.id)+"-" + date.today().strftime("%Y-%m-%d")+'.xlsx'
            await generate_xlfile(data, filename)
            await send_mail(alert.username, 'Daily report', "this is your daily report", filename, 'cname.xlsx')
            await update_last_time_notified(alert.id)
