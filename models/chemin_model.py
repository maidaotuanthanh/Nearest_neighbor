from pydantic import BaseModel
from datetime import datetime


class Chemin(BaseModel):
    WaveID: int
    Distance_Route: float
    Chemins: list
    Orders_Number: list

