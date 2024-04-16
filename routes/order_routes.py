import pandas as pd
from ast import literal_eval
import itertools
from fastapi import APIRouter
from models.order_model import Order
from schemas.order_schema import order_serializer, orders_serializer
from config.db import conn

order = APIRouter()


def orderlines_mapping(df_orderlines, orders_number):
    # Sắp xếp các đơn hàng theo thứ tự thời gian trên hệ thống
    df_orderlines = df_orderlines.sort_values(by='DATE', ascending=True)
    # Tạo list những đơn hàng duy nhất (unique) theo mã đơn (OrderNumber)
    list_orders = df_orderlines['OrderNumber'].unique()
    # Tạo ra dictionary với key là mã đơn và value là số thứ tự tăng dần (gọi là OrderID)
    dict_map = dict(zip(list_orders, [i for i in range(1, len(list_orders) + 1)]))
    # Tạo cột OrderID trong DataFrame theo dictionary đã tạo
    df_orderlines['OrderID'] = df_orderlines['OrderNumber'].map(dict_map)
    # Tạo cột WaveID theo công thức đã nêu ở trên
    df_orderlines['WaveID'] = ((df_orderlines['OrderID'] + (orders_number - 1)) // orders_number) - 1
    # Đếm số lượng wave của DataFrame
    waves_number = df_orderlines.WaveID.max() + 1
    # print(waves_number)
    # print(df_orderlines)
    return df_orderlines, waves_number


def locations_listing(df_orderlines, wave_id):
    # Lọc ra từ Dataframe theo với mã wave muốn list
    df = df_orderlines[df_orderlines.WaveID == wave_id]

    # Tạo list tọa độ bằng xử lý chuỗi
    list_locs = list(df['Coord'].apply(lambda t: literal_eval(t)).values)
    list_locs = list(k for k, _ in itertools.groupby(list_locs))

    # Tính độ dài của list
    n_locs = len(list_locs)
    # print(list_locs)
    return list_locs, n_locs


def distance_picking(Loc1, Loc2, y_low, y_high):
    # Tọa độ điểm đầu
    x1, y1 = Loc1[0], Loc1[1]
    # Tọa độ điểm cuối
    x2, y2 = Loc2[0], Loc2[1]
    # Khoảng cách trục x
    distance_x = abs(x2 - x1)
    route_1 = [(x1, y_high), (x2, y_high)]
    route_2 = [(x1, y_low), (x2, y_low)]
    route_0 = []
    # Khoảng cách trục y (có 2 khoảng cách do có 2 cách di chuyển)
    if x1 == x2:
        distance_y1 = abs(y2 - y1)
        distance_y = distance_y1
        route = route_0
    else:
        distance_y1 = (y_high - y1) + (y_high - y2)
        distance_y2 = (y1 - y_low) + (y2 - y_low)
        # Chọn khoảng cách trục y ngắn nhất
        if distance_y1 < distance_y2:
            distance_y = distance_y1
            route = route_1
        else:
            distance_y = distance_y2
            route = route_2
    # Tổng khoảng cách
    distance = distance_x + distance_y
    # print x1,y1 and route and x2, y2 in one line
    # print("route: ", route)
    # if x1,y1 in route or x2,y2 in route: delete in route
    if (x1, y1) in route:
        route.remove((x1, y1))
    if (x2, y2) in route:
        route.remove((x2, y2))
    # print("x1, y1: ", x1, y1, "route: ", route, "x2, y2: ", x2, y2)
    return distance, route


def next_location(start_loc, list_locs, y_low, y_high):
    list_dist = []
    list_route = []
    for loc in list_locs:
        dist, route = distance_picking(start_loc, loc, y_low, y_high)
        list_dist.append(dist)
        list_route.append(route)
    # list_dist = [distance_picking(start_loc, loc, y_low, y_high) for loc in list_locs]
    distance_next = min(list_dist)

    index_min = list_dist.index(min(list_dist))
    next_loc = list_locs[index_min]
    route = list_route[index_min]
    list_locs.remove(next_loc)
    return list_locs, next_loc, next_loc, distance_next, route


def create_picking_route(origin_loc, list_locs, y_low, y_high):
    wave_distance = 0
    start_loc = origin_loc
    list_chemin = []
    list_chemin.append(start_loc)
    while len(list_locs) > 0:
        list_locs, start_loc, next_loc, distance_next, route = next_location(start_loc, list_locs, y_low, y_high)
        start_loc = next_loc
        for i in range(len(route)):
            x, y = route[i]
            list_chemin.append([x, y])
        list_chemin.append(next_loc)
        wave_distance = wave_distance + distance_next
    dist, route = distance_picking(start_loc, origin_loc, y_low, y_high)
    # wave_distance = wave_distance + distance_picking(start_loc, origin_loc, y_low, y_high)
    wave_distance = wave_distance + dist
    for i in range(len(route)):
        x, y = route[i]
        list_chemin.append([x, y])

    list_chemin.append(origin_loc)
    # print(list_chemin)
    return wave_distance, list_chemin


def simulation_wave(y_low, y_high, orders_number, df_orderlines, list_wid, list_dst, list_route, list_ord):
    # Địa điểm ban đầu ( khu vực xuất hàng - cửa kho)
    Loc_orn = [0, y_low]
    # Tạp biến để lưu tổng khoảng cách
    distance_route = 0
    # Tạp wave từ DataFrame đọc được bằng hàm orderlines_maping đã viết
    df_orderlines, waves_number = orderlines_mapping(df_orderlines, orders_number)
    # Thực hiện vòng lặp tìm route cho mỗi wave
    for wave_id in range(waves_number):
        # List ra các location cho mỗi wave
        list_locs, n_locs = locations_listing(df_orderlines, wave_id)
        # Sử dụng hàm create_picking_route để tạo
        wave_distance, list_chemin = create_picking_route(Loc_orn, list_locs, y_low, y_high)
        distance_route = distance_route + wave_distance
        # Thêm các kết quả sau mỗi vòng lặp vào các list
        list_wid.append(wave_id)
        list_dst.append(wave_distance)
        list_route.append(list_chemin)
        list_ord.append(orders_number)

    # print(list_route)
    # print(list_route)
    # print("\n --------------------------------------------------")
    return list_wid, list_dst, list_route, list_ord, distance_route


# get all orders
@order.get("/orders")
async def get_orders():
    # print(conn.local.order.find())
    # print(orders_serializer(conn.local.order.find()))
    # print(orders_serializer(conn.local.order.find()))
    return orders_serializer(conn.local.order.find())


@order.get("/get_route_picking")
async def get_route_picking():
    result = orders_serializer(conn.local.order.find())
    df_orderlines = pd.DataFrame(result)

    print(df_orderlines.iloc[0]['Coord'][0])
    # df_orderlines = pd.read_csv('df_lines.csv')
    y_low, y_high = 0, 25
    # list_wid, list_dst, list_route, list_ord = [], [], [], []
    for orders_numbers in range(1, 7):
        list_wid, list_dst, list_route, list_ord, distance_route = simulation_wave(y_low, y_high, orders_numbers, df_orderlines, list_wid, list_dst, list_route, list_ord)
        print("Total distance covered for {} orders/wave: {:,} m".format(orders_numbers, distance_route))
    # df_results = pd.DataFrame(
        # {'Wave_Number': list_wid, 'Distance_Route': list_dst, 'Chemins': list_route})
    # print(df_results)
    # df_results.to_csv('output1.csv', index=False)
    # return {"status": "Ok", "data": "Route Picking"}
    # return df_orderlines
    # return result
    return 1