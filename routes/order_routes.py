import pandas as pd
from ast import literal_eval
import itertools
from fastapi import APIRouter
from models.order_model import Order
from schemas.order_schema import order_serializer, orders_serializer
from config.db import conn

order = APIRouter()


# api add data order to database
# @picking.post("/add_order")
# async def add_order():
#     # Define the data to be inserted
#     data = [
#         {
#             "STT": 11,
#             "OrderNumber": 3,
#             "ProductID": "A0322",
#             "QuantityOrder": 5,
#             "Order": 3,
#             "Date": "12/11/2018"
#         }]
#     # Insert the data and get the InsertManyResult object
#     insert_result = conn.local.order.insert_many(data)
#
#     # Retrieve the inserted documents using the inserted_ids
#     new_orders = conn.local.order.find({"_id": {"$in": insert_result.inserted_ids}})
#
#     # Serialize the inserted documents
#     new_results = orders_serializer(new_orders)
#
#     return new_results

# get all orders
async def get_orders():
    # print(conn.local.order.find())
    # print(orders_serializer(conn.local.order.find()))
    # print(orders_serializer(conn.local.order.find()))
    return orders_serializer(conn.local.order.find())
