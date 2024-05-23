import pandas as pd
from ast import literal_eval
import itertools
from fastapi import APIRouter
from models.layout_model import Layout
from schemas.layout_schema import layout_serializer, layouts_serializer
from config.db import conn

layout = APIRouter()


# api add data layout to database
# @layout.post("/add_layout")
# async def add_layout():
#     # Define the data to be inserted
#     data = [
#         {
#             "STT": 100,
#             "PCS": 2,
#             "Location": "A0608204",
#             "Alley_Number": "A06",
#             "Quantity": 20,
#             "Coord": [
#                 34.5,
#                 12,
#                 1
#             ],
#             "ProductID": "A0608",
#             "DateProduct": "12/11/2018"
#         }
#     ]
#     # Insert the data and get the InsertManyResult object
#     insert_result = conn.local.layout.insert_many(data)
#
#     # Retrieve the inserted documents using the inserted_ids
#     new_layouts = conn.local.layout.find({"_id": {"$in": insert_result.inserted_ids}})
#
#     # Serialize the inserted documents
#     new_results = layouts_serializer(new_layouts)
#
#     return new_results

# get all layouts
# @layout.get("/layouts")
# async def get_layouts():
#     return layouts_serializer(conn.local.layout.find())
#
async def get_layouts():
    return layouts_serializer(conn.local.layout.find())
