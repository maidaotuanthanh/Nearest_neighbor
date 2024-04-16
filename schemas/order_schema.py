def order_serializer(order) -> dict:
    return {
        "id": str(order["_id"]),
        'STT': str(order["STT"]),
        'DATE': order["DATE"],
        'OrderNumber': order["OrderNumber"],
        'SKU': order["SKU"],
        'PCS': order["PCS"],
        'ReferenceID': order["ReferenceID"],
        'Location': str(order["Location"]),
        'Alley_Number': str(order["Alley_Number"]),
        'Cellule': order["Cellule"],
        'Coord': order["Coord"],
        'AlleyCell': str(order["AlleyCell"])

    }


def orders_serializer(orders) -> list:
    return [order_serializer(order) for order in orders]
