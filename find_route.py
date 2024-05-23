import itertools
from ast import literal_eval
import pandas as pd
import json


def orderlines_mapping(df_orderlines, orders_number):
    # Đọc dữ liệu từ file csv
    # Sắp xếp dữ liệu theo 'Order'
    df_order_sorted = df_orderlines.sort_values(by='STT')
    list_orders = df_orderlines['OrderNumber'].unique()
    # Tạo cột 'Wave' dựa trên 'Order', mỗi wave bao gồm 3 đơn hàng
    dict_map = dict(zip(list_orders, list_orders))
    # Tạo cột OrderID trong DataFrame theo dictionary đã tạo
    df_orderlines['OrderID'] = df_orderlines['OrderNumber'].map(dict_map)
    # Tạo cột WaveID theo công thức đã nêu ở trên
    df_orderlines['WaveID'] = ((df_orderlines['Order'] + (orders_number - 1)) // orders_number)
    waves_number = df_orderlines.WaveID.max() + 1
    return df_orderlines, waves_number


def get_product_layout(df_orderlines, df_layout, orders_number):
    df_orderlines, waves_number = orderlines_mapping(df_orderlines, orders_number)
    df_orderlines = df_orderlines.sort_values(by='OrderNumber')
    df_grouped = df_orderlines.groupby(['WaveID', 'ProductID'])['QuantityOrder'].sum().reset_index()
    # print(df_orderlines)
    df_layout['SubProductID'] = df_layout.groupby('ProductID').cumcount() + 1
    df_layout['SubProductID'] = df_layout['ProductID'] + '_' + df_layout['SubProductID'].astype(str)

    df_final = pd.DataFrame()  # Tạo DataFrame rỗng
    wave_order_ids = df_orderlines.groupby('WaveID')['OrderID'].apply(list)  # Tạo mảng chứa các OrderID của từng wave
    wave_order_ids_dict = wave_order_ids.to_dict()  # Chuyển đổi Series thành dictionary

    for wave_id in range(1, waves_number):
        df_grouped_wave = df_grouped[df_grouped['WaveID'] == wave_id]
        product_ids_in_grouped = df_grouped_wave['ProductID']
        df_compare = df_layout[df_layout['ProductID'].isin(product_ids_in_grouped)]
        df_compare = df_compare.sort_values(['ProductID', 'SubProductID'])
        df_compare['QuantityTaken'] = 0
        for index, row in df_compare.iterrows():
            product_id = row['ProductID']
            quantity_needed = df_grouped_wave.loc[df_grouped_wave['ProductID'] == product_id, 'QuantityOrder'].values[0]

            if quantity_needed > row['Quantity']:
                df_grouped_wave.loc[df_grouped_wave['ProductID'] == product_id, 'QuantityOrder'] -= row['Quantity']
                df_compare.loc[index, 'QuantityTaken'] = row['Quantity']
                df_compare.loc[index, 'Quantity'] = 0
            else:
                df_grouped_wave.loc[df_grouped_wave['ProductID'] == row['ProductID'], 'QuantityOrder'] = 0
                df_compare.loc[index, 'QuantityTaken'] = quantity_needed
                df_compare.loc[index, 'Quantity'] -= quantity_needed

            # Thêm OrderID vào df_compare
            # df_compare.at[index, 'OrderID'] = order_id
        df_compare = df_compare[df_compare['QuantityTaken'] != 0]
        df_compare = df_compare.sort_values('STT')
        df_compare['WaveID'] = wave_id  # Thêm cột 'WaveID'
        df_final = pd.concat([df_final, df_compare])  # Nối df_compare với df_final

        # Cập nhật số lượng trong df_layout sau mỗi wave
        for index, row in df_compare.iterrows():
            df_layout.loc[(df_layout['ProductID'] == row['ProductID']) & (
                    df_layout['SubProductID'] == row['SubProductID']), 'Quantity'] = row['Quantity']

    # df_final.to_csv('df_compare_final.csv', index=False)  # Lưu df_final vào file csv

    return df_final, waves_number, wave_order_ids_dict


# List ra những location của một mã wave
def locations_listing(df_final, wave_id):
    # Lọc ra từ Dataframe theo với mã wave muốn list
    df = df_final[df_final['WaveID'] == wave_id]
    # Tạo list tọa độ bằng xử lý chuỗi
    list_locs = list(df['Coord'].apply(lambda t: literal_eval(t)).values)
    # list_locs = df['Coord'].tolist()
    # print(list_locs)
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
    list_chemin.append(start_loc if len(start_loc) == 3 else start_loc + [0])
    while len(list_locs) > 0:
        list_locs, start_loc, next_loc, distance_next, route = next_location(start_loc, list_locs, y_low, y_high)
        start_loc = next_loc
        for i in range(len(route)):
            x, y = route[i]
            list_chemin.append([x, y, 0])
        list_chemin.append(next_loc if len(next_loc) == 3 else next_loc + [0])
        wave_distance = wave_distance + distance_next
    dist, route = distance_picking(start_loc, origin_loc, y_low, y_high)
    # wave_distance = wave_distance + distance_picking(start_loc, origin_loc, y_low, y_high)
    wave_distance = wave_distance + dist
    for i in range(len(route)):
        x, y = route[i]
        list_chemin.append([x, y, 0])

    list_chemin.append(origin_loc if len(origin_loc) == 3 else origin_loc + [0])
    # print(list_chemin)
    return wave_distance, list_chemin


def simulation_wave(y_low, y_high, orders_number, df_orderlines, wave_route, list_dst, list_route, df_layout):
    # Địa điểm ban đầu ( khu vực xuất hàng, cửa hàng)
    Loc_orn = [0, y_low]
    # Tạo biến để lưu tổng khoảng cách
    distance_route = 0
    # print(df_orderlines)
    # Lấy wave từ get_product_layout
    df_final, waves_number, wave_order_ids_dict = get_product_layout(df_orderlines, df_layout, orders_number)
    # print(wave_order_ids_dict)
    # print(df_final)
    order_ids_route = []  # Tạo danh sách mới để lưu OrderID

    for wave_id in range(1, waves_number):
        # List ra các location cho mỗi wave
        list_locs, n_locs = locations_listing(df_final, wave_id)
        # Sử dụng hàm create_picking_route để tạo
        wave_distance, list_chemin = create_picking_route(Loc_orn, list_locs, y_low, y_high)
        distance_route = distance_route + wave_distance
        list_dst.append(wave_distance)
        list_route.append(list_chemin)
        wave_route.append(wave_id)
        # print(wave_id)

        # Loại bỏ các OrderID trùng lặp
        unique_order_ids = list(set(wave_order_ids_dict[wave_id]))
        unique_order_ids.sort()
        wave_order_ids_dict[wave_id] = unique_order_ids
        print(f"For wave_id {wave_id}, the unique OrderIDs are: {unique_order_ids}")
        order_ids_route.append(unique_order_ids)

    return wave_route, list_dst, list_route, distance_route, order_ids_route


df_orderlines = pd.read_json('database/df_order.json')
orders_numbers = 1
df_layout = pd.read_json('database/df_layout.json')
y_low, y_high = 0, 25
wave_route, list_dst, list_route = [], [], []
wave_route, list_dst, list_route, distance_route, order_ids_route = simulation_wave(y_low, y_high,
                                                                   orders_numbers,
                                                                   df_orderlines,
                                                                   wave_route,
                                                                   list_dst,
                                                                   list_route, df_layout)

df_results = pd.DataFrame({'WaveID': wave_route, 'Distance_Route': list_dst, 'Chemins': list_route, 'Orders_Number': order_ids_route})
# df_last_orders_number = df_results[df_results['Orders_Number'] == orders_numbersf]
df_results.to_csv('output/output_2.csv', index=False)
