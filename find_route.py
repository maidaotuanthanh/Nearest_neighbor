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


df_orderlines = pd.read_csv('df_order.csv')
orders_number = 3
df_orderlines, waves_number = orderlines_mapping(df_orderlines, orders_number)

# Nhóm các 'ProductID' giống nhau và cộng các 'Quantity' của các 'Order' có cùng 'ProductID'
df_grouped = df_orderlines.groupby(['WaveID', 'ProductID'])['QuantityOrder'].sum().reset_index()

# In kết quả
# print(df_grouped)
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
df_compare = pd.read_csv('df_compare.csv')
# df_compare = df_layout
product_ids_in_grouped = df_grouped['ProductID']
df_compare = df_compare[df_compare['ProductID'].isin(product_ids_in_grouped)]
df_compare = df_compare.sort_values(['ProductID', 'SubProductID'])
# Duyệt qua từng hàng của df_compare
# Thêm cột mới 'QuantityTaken' vào df_compare để theo dõi số lượng sản phẩm đã lấy từ mỗi pallet
df_compare['QuantityTaken'] = 0

# Duyệt qua từng hàng của df_compare
for index, row in df_compare.iterrows():
    # Lấy số lượng sản phẩm cần lấy từ df_grouped
    quantity_needed = df_grouped.loc[df_grouped['ProductID'] == row['ProductID'], 'QuantityOrder'].values[0]

    # Kiểm tra xem số lượng sản phẩm cần lấy có lớn hơn số lượng sản phẩm trong pallet không
    if quantity_needed > row['Quantity']:
        # Nếu có, lấy tất cả sản phẩm trong pallet và giảm số lượng sản phẩm cần lấy
        print(f"Lấy tất cả {row['Quantity']} sản phẩm {row['ProductID']} từ pallet tại tọa độ {row['Coord']}")
        df_grouped.loc[df_grouped['ProductID'] == row['ProductID'], 'QuantityOrder'] -= row['Quantity']
        df_compare.loc[index, 'QuantityTaken'] = row['Quantity']
        df_compare.loc[index, 'Quantity'] = 0
    else:
        # Nếu không, chỉ lấy số lượng sản phẩm cần lấy
        print(f"Lấy {quantity_needed} sản phẩm {row['ProductID']} từ pallet tại tọa độ {row['Coord']}")
        df_grouped.loc[df_grouped['ProductID'] == row['ProductID'], 'QuantityOrder'] = 0
        df_compare.loc[index, 'QuantityTaken'] = quantity_needed
        df_compare.loc[index, 'Quantity'] -= quantity_needed

# Lọc df_compare để chỉ giữ lại các dòng có 'QuantityTaken' khác 0
# df_compare = df_compare[df_compare['QuantityTaken'] != 0]

# Lưu df_compare vào file csv
df_compare.to_csv('df_compare_updated.csv', index=False)