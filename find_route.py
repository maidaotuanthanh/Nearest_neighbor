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
print(df_grouped)
# print(df_orderlines)
