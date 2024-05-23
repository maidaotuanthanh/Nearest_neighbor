import pandas as pd
from ast import literal_eval
import itertools
from fastapi import APIRouter

from endpoints.nearest_neighbor import simulation_wave
from models.order_model import Order
from routes.order_routes import get_orders
from schemas.order_schema import order_serializer, orders_serializer
from models.layout_model import Layout
from routes.layout_routes import get_layouts
from schemas.layout_schema import layout_serializer, layouts_serializer
from models.chemin_model import Chemin
from schemas.chemin_schema import chemin_serializer, chemins_serializer
from config.db import conn

picking = APIRouter()


@picking.get("/simulate_wave/{orders_numbers}")
async def simulate_wave_api(orders_numbers: int):
    df_layout = await get_layouts()
    df_orderlines = await get_orders()
    # df_orderlines = pd.read_json('../database/df_order.json')
    # orders_numbers = 3
    # df_layout = pd.read_json('database/df_layout.json')
    y_low, y_high = 0, 25
    wave_route, list_dst, list_route = [], [], []
    wave_route, list_dst, list_route, distance_route, order_ids_route = simulation_wave(y_low, y_high,
                                                                                        orders_numbers,
                                                                                        df_orderlines,
                                                                                        wave_route,
                                                                                        list_dst,
                                                                                        list_route, df_layout)

    df_results = pd.DataFrame(
        {'WaveID': wave_route, 'Distance_Route': list_dst, 'Chemins': list_route, 'Orders_Number': order_ids_route})
    # df_results.to_json('output/output_2.json', orient='records')
    results_dict = df_results.to_dict(orient='records')

    conn.local.chemin.delete_many({})

    insert_result = conn.local.chemin.insert_many(results_dict)
    # new_chemins = conn.local.chemin.find({"_id": {"$in": insert_result.inserted_ids}})

    # Serialize the inserted documents
    # new_results = chemins_serializer(new_chemins)
    # return success message
    return {"message": "Success"}
