from turtle import st

import numpy as np
import pandas as pd
from ast import literal_eval
import itertools

# Đầu tiên là dựa vào OrderNumber (ở đây là kiểu ID của order đấy) để tạo ra OrderID, OrderID này sẽ tăng dần từ 1 cho mỗi order mới.
# Tạo thêm cột WaveID trong DataFrame để đánh dấu những đơn hàng chung một wave
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
    # df_orderlines['WaveID'] = ((df_orderlines['OrderID'] + (orders_number - 1)) // orders_number) - 1
    df_orderlines['WaveID'] = (df_orderlines['OrderID'] % orders_number == 0).shift(1).fillna(0).cumsum()
    # Đếm số lượng wave của DataFrame
    waves_number = df_orderlines.WaveID.max() + 1
    # print(waves_number)
    # print(df_orderlines)
    # create file csv after add WaveID and OrderID
    df_orderlines.to_csv('orders_2.csv', index=False)
    return df_orderlines, waves_number


# List ra những location của một mã wave
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


# Tính khoảng cách giữa 2 điểm lấy hàng trong kho
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


# Chương trình gom các lượng đơn hàng mỗi wave khác nhau
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

def simulate_batch(n1, n2, y_low, y_high, origin_log, orders_number, df_orderlines):
    # Lists for results
    list_wid, list_dst, list_route, list_ord = [], [], [], []
    # Test several values of orders per wave
    for orders_number in range(n1, n2 + 1):
        list_wid, list_dst, list_route, list_ord, distance_route = simulation_wave(y_low, y_high, orders_number, df_orderlines, list_wid, list_dst, list_route, list_ord)
        print("Total distance covered for {} orders/wave: {:,} m".format(orders_number, distance_route))

    # By Wave
    df_waves = pd.DataFrame({'wave': list_wid,
                'distance': list_dst,
                'routes': list_route,
                'order_per_wave': list_ord})

    # Results aggregate
    df_results = pd.DataFrame(df_waves.groupby(['order_per_wave'])['distance'].sum())
    df_results.columns = ['distance']
    return df_waves, df_results.reset_index()

df_orderlines = pd.read_csv('df_lines_full.csv')

n = st.slider(
    'SIMULATION 1 SCOPE (THOUSDAND ORDERS)', 1, 200, value=5)

y_low, y_high = 0, 25
origin_loc = [0, y_low]
lines_number = 1000 * n
n1 = st.slider(
    'SIMULATION 1: N_MIN (ORDERS/WAVE)', 0, 20, value=1)
n2 = st.slider(
    'SIMULATION 1: N_MAX (ORDERS/WAVE)', n1 + 1, 20, value=int(np.max([n1 + 1, 10])))
df_waves, df_results = simulate_batch(n1, n2, y_low, y_high, origin_loc, lines_number, df_orderlines)
print(df_waves)
# list_wid, list_dst, list_route, list_ord = [], [], [], []
#
# for orders_numbers in range(1, 7):
#     list_wid, list_dst, list_route, list_ord, distance_route = simulation_wave(y_low, y_high, orders_numbers, df_orderlines, list_wid, list_dst, list_route, list_ord)
#     print("Total distance covered for {} orders/wave: {:,} m".format(orders_numbers, distance_route))
#
# df_results = pd.DataFrame(
#     {'Wave_Number': list_wid, 'Distance_Route': list_dst, 'Chemins': list_route, 'Orders_Number': list_ord})
# print(df_results)
# df_results.to_csv('output_2.csv', index=False)
