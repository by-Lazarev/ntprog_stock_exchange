from pydantic import BaseModel
from datetime import datetime

from enums import *


class OrderBase(BaseModel):
    creation_time: datetime
    change_time: datetime
    status: OrderStatus
    side: OrderSide
    price: float  # Change on decimal, as it is money
    amount: int
    instrument: Instrument
    user_id: int
    uuid: str
