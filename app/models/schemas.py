from typing import List
from pydantic import BaseModel
from datetime import date
from enum import Enum


class Kpi(str, Enum):
    price = 'price'
    stars = 'stars'


class AddAlertInfoSchema(BaseModel):

    username: str
    superproduct_ids: List[int]
    chain_ids: List[int]
    last_time_notified: date = date.today().strftime("%Y-%m-%d")
    frequency: int
    threshold: float
    kpi: Kpi


class AlertInfoSchema(AddAlertInfoSchema):
    id: int
