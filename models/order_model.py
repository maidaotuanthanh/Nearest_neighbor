from pydantic import BaseModel
from datetime import datetime


class Order(BaseModel):
    STT: str
    DATE: datetime
    OrderNumber: int
    SKU: int
    PCS: int
    ReferenceID: int
    Location: str
    Alley_Number: str
    Cellule: int
    Coord: list
    AlleyCell: str
