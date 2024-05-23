from pydantic import BaseModel
from datetime import datetime


class Order(BaseModel):
    STT: str
    OrderNumber: int
    ProductID: str
    QuantityOrder: int
    Order: int
    Date: datetime
