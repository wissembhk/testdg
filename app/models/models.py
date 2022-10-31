from utils.database import base
from sqlalchemy import Column,  Integer, Date, Float, Enum, String, ARRAY, UniqueConstraint
from models.schemas import Kpi


class PlatformAlert(base):
    __tablename__ = "platform_alert"
    id = Column(Integer, primary_key=True, auto_increment=True)
    username = Column(String)
    superproduct_ids = Column(ARRAY(Integer))
    chain_ids = Column(ARRAY(Integer))
    last_time_notified = Column(Date)
    frequency = Column(Integer)
    threshold = Column(Float)
    kpi = Column(Enum(Kpi))
    UniqueConstraint(superproduct_ids, chain_ids, username)
