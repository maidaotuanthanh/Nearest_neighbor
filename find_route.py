import pandas as pd


def orderlines_mapping(df_orderlines, orders_number):
    # Đọc dữ liệu từ file csv
    # Sắp xếp dữ liệu theo 'Order'
    df_order_sorted = df_orderlines.sort_values(by='STT')
    list_orders = df_orderlines['OrderNumber'].unique()
    # Tạo cột 'Wave' dựa trên 'Order', mỗi wave bao gồm 3 đơn hàng
    dict_map = dict(zip(list_orders, [i for i in range(1, len(list_orders) + 1)]))
    # Tạo cột OrderID trong DataFrame theo dictionary đã tạo
    df_orderlines['OrderID'] = df_orderlines['OrderNumber'].map(dict_map)
    # Tạo cột WaveID theo công thức đã nêu ở trên
    df_orderlines['WaveID'] = ((df_orderlines['OrderID'] + (orders_number - 1)) // orders_number)
    waves_number = df_orderlines.WaveID.max() + 1
    # In kết quả
    # print(df_order_sorted)
    return df_orderlines, waves_number

# List ra những location của một mã wave
def locations_listing(df_orderlines, wave_id):
    # Lọc ra từ Dataframe theo với mã wave muốn list
    df = df_orderlines[df_orderlines.WaveID == wave_id]

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


df_orderlines = pd.read_csv('df_order.csv')
orders_number = 3
df_orderlines, waves_number = orderlines_mapping(df_orderlines, orders_number)

# Nhóm các 'ProductID' giống nhau và cộng các 'Quantity' của các 'Order' có cùng 'ProductID'
df_grouped = df_orderlines.groupby(['WaveID', 'ProductID'])['QuantityOrder'].sum().reset_index()

# In kết quả
print(df_grouped)
# print(df_orderlines)
# Đọc dữ liệu từ file df_layout.csv
df_layout = pd.read_csv('df_layout.csv')

# Trích xuất cột 'ProductID' từ df_grouped
# product_ids_in_grouped = df_grouped['ProductID']
#
# # Lọc df_layout dựa trên product_ids_in_grouped
# df_layout_with_products_in_grouped = df_layout[df_layout['ProductID'].isin(product_ids_in_grouped)]
#
# # In kết quả
# print(df_layout_with_products_in_grouped)
# Tạo cột 'SubProductID' dựa trên số thứ tự của mỗi 'ProductID' trong nhóm của nó
df_layout['SubProductID'] = df_layout.groupby('ProductID').cumcount() + 1

# Tạo cột 'SubProductID' mới bằng cách nối cột 'ProductID' với cột 'SubProductID'
df_layout['SubProductID'] = df_layout['ProductID'] + '_' + df_layout['SubProductID'].astype(str)

# In kết quả
# print to csv
# df_layout.to_csv('df_compare.csv', index=False)
# print(df_layout)
# df_compare = pd.read_csv('df_compare.csv')
df_compare = df_layout
product_ids_in_grouped = df_grouped['ProductID']
df_compare = df_compare[df_compare['ProductID'].isin(product_ids_in_grouped)]
df_compare = df_compare.sort_values(['ProductID', 'SubProductID'])
# Duyệt qua từng hàng của df_compare
# Thêm cột mới 'QuantityTaken' vào df_compare để theo dõi số lượng sản phẩm đã lấy từ mỗi pallet
df_compare['QuantityTaken'] = 0

# Sắp xếp df_compare theo cột 'Quantity' theo thứ tự tăng dần
# df_compare = df_compare.sort_values('Quantity')

# Duyệt qua từng hàng của df_compare
for index, row in df_compare.iterrows():
    # Lấy số lượng sản phẩm cần lấy từ df_grouped
    quantity_needed = df_grouped.loc[df_grouped['ProductID'] == row['ProductID'], 'QuantityOrder'].values[0]

    # Kiểm tra xem số lượng sản phẩm cần lấy có lớn hơn số lượng sản phẩm trong pallet không
    if quantity_needed > row['Quantity']:
        # Nếu có, lấy tất cả sản phẩm trong pallet và giảm số lượng sản phẩm cần lấy
        df_grouped.loc[df_grouped['ProductID'] == row['ProductID'], 'QuantityOrder'] -= row['Quantity']
        df_compare.loc[index, 'QuantityTaken'] = row['Quantity']
        df_compare.loc[index, 'Quantity'] = 0
    else:
        # Nếu không, chỉ lấy số lượng sản phẩm cần lấy
        df_grouped.loc[df_grouped['ProductID'] == row['ProductID'], 'QuantityOrder'] = 0
        df_compare.loc[index, 'QuantityTaken'] = quantity_needed
        df_compare.loc[index, 'Quantity'] -= quantity_needed

# Lọc df_compare để chỉ giữ lại các dòng có 'QuantityTaken' khác 0
df_sorted = df_compare.sort_values('STT')

# Lưu df_compare vào file csv
df_sorted.to_csv('df_compare_updated.csv', index=False)
