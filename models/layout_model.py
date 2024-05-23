from pydantic import BaseModel
from datetime import datetime


class Layout(BaseModel):
    STT: str
    PCS: int
    Location: str
    Alley_Number: str
    Quantity: int
    Coord: list
    ProductID: str
    DateProduct: datetime
