def order_serializer(order) -> dict:
    return {
        "id": str(order["_id"]),
        'STT': str(order["STT"]),
        'OrderNumber': order["OrderNumber"],
        'ProductID': order["ProductID"],
        'QuantityOrder': order["QuantityOrder"],
        'Order': order["Order"],
        'Date': order["Date"]
    }


def orders_serializer(orders) -> list:
    return [order_serializer(order) for order in orders]
