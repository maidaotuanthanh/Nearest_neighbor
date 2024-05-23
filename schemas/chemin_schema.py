def chemin_serializer(chemin) -> dict:
    return {
        "id": str(chemin["_id"]),
        "WaveID": int(chemin["WaveID"]),
        "Distance_Route": float(chemin["Distance_Route"]),
        "Chemins": list(chemin["Chemins"]),
        "Orders_Number": list(chemin["Orders_Number"])
    }


def chemins_serializer(chemins) -> list:
    return [chemin_serializer(chemin) for chemin in chemins]