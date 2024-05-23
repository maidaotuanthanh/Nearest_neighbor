def layout_serializer(layout) -> dict:
    return {
        "id": str(layout["_id"]),
        'STT': str(layout["STT"]),
        'PCS': layout["PCS"],
        'Location': str(layout["Location"]),
        'Alley_Number': str(layout["Alley_Number"]),
        'Quantity': int(layout["Quantity"]),
        'Coord': layout["Coord"],
        'ProductID': layout["ProductID"],
        'DateProduct': layout["DateProduct"]

    }


def layouts_serializer(layouts) -> list:
    return [layout_serializer(layout) for layout in layouts]