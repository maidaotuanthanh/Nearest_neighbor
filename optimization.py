class Product:
    def __init__(self, id, name, pallet_id=None, quantity=1):
        self.id = id
        self.name = name
        self.pallet_id = pallet_id
        self.quantity = quantity


class Pallet:
    def __init__(self, id, x, y, z, capacity, product_id=None):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.capacity = capacity
        self.product_id = product_id  # ID của sản phẩm trong pallet, nếu có
        self.current_quantity = 0  # Số lượng hiện tại của sản phẩm trong pallet


def optimize_storage(products, pallets):
    used_storage = {}
    pallet_product_map = {}  # Dictionary to keep track of which pallets are used by which product types
    product_quantity_map = {}  # Dictionary to keep track of the total quantity of each product type that will be stored in each pallet

    # Iterate over the products
    for product in products.values():
        if product.pallet_id is not None:
            pallet = pallets.get(product.pallet_id)
            if pallet is not None and pallet.capacity > 0:
                used_storage[product] = pallet
                pallet_product_map[pallet.id] = product.name  # Update the product type for this pallet
                product_quantity_map[product.name] = product_quantity_map.get(product.name, 0) + product.quantity  # Update the total quantity of this product type

    # Iterate over the products again for the new products
    for product in products.values():
        if product.pallet_id is None:
            best_fit_pallet = None
            min_distance = float('inf')

            # Find the nearest pallet for the new product
            for pallet in pallets.copy().values():
                if pallet.capacity > 0:
                    # Check if this pallet is already used by a different product type
                    if pallet.id in pallet_product_map and pallet_product_map[pallet.id] != product.name:
                        continue  # Skip this pallet

                    # Check if the total quantity of this product type, including the current product, exceeds the capacity of the pallet
                    total_quantity = product_quantity_map.get(product.name, 0) + product.quantity
                    if total_quantity > pallet.capacity:
                        # If the total quantity exceeds the capacity, try to find another pallet with enough remaining capacity
                        for other_pallet in pallets.values():
                            if other_pallet.capacity - product_quantity_map.get(pallet_product_map.get(other_pallet.id), 0) >= product.quantity:
                                used_storage[product] = other_pallet
                                pallet_product_map[other_pallet.id] = product.name  # Update the product type for this pallet
                                product_quantity_map[product.name] = product_quantity_map.get(product.name, 0) + product.quantity  # Update the total quantity of this product type
                                break
                        else:
                            # If no other pallet has enough remaining capacity, create a new pallet
                            new_pallet = create_new_pallet(pallets)
                            used_storage[product] = new_pallet
                            pallet_product_map[new_pallet.id] = product.name  # Update the product type for this pallet
                            product_quantity_map[product.name] = product_quantity_map.get(product.name, 0) + product.quantity  # Update the total quantity of this product type
                        continue  # Skip this pallet

                    distance = calculate_distance(pallet, (0, 0, 0))
                    if distance < min_distance:
                        best_fit_pallet = pallet
                        min_distance = distance

            # If a suitable pallet is found, place the product in that pallet
            if best_fit_pallet is not None:
                used_storage[product] = best_fit_pallet
                pallet_product_map[best_fit_pallet.id] = product.name  # Update the product type for this pallet
                product_quantity_map[product.name] = product_quantity_map.get(product.name, 0) + product.quantity  # Update the total quantity of this product type

    return used_storage

def calculate_distance(pallet, destination):
    # Tính khoảng cách giữa pallet và điểm đích
    return ((pallet.x - destination[0]) ** 2 + (pallet.y - destination[1]) ** 2 + (
                pallet.z - destination[2]) ** 2) ** 0.5


def create_new_pallet(pallets):
    # Tạo một pallet mới với id là số tiếp theo của pallets
    new_pallet_id = max(pallets.keys()) + 1  # Change this line
    new_pallet = Pallet(new_pallet_id, 0, 0, 0, capacity=10)  # Giả sử dung lượng của pallet mới là 10
    pallets[new_pallet_id] = new_pallet
    return new_pallet


# Danh sách các sản phẩm và thông tin về chúng
products = {
    1: Product(1, "A", pallet_id=1),
    2: Product(2, "B", pallet_id=2),
    3: Product(3, "C", quantity=2),
    4: Product(4, "D", quantity=3),
    5: Product(1, "A", quantity=2),
    6: Product(2, "B", quantity=1),
    7: Product(1, "A", quantity=2),
    8: Product(2, "B", quantity=1),
    9: Product(2, "B", quantity=5),
    10: Product(2, "B", quantity=10),
    11: Product(5, "E", quantity=10),
    12: Product(5, "E", quantity=10)
}

# Danh sách các pallet và thông tin về chúng
# Giả sử đã có 2 pallet đã chứa hàng hóa trong kho
pallets = {
    1: Pallet(1, 10, 10, 10, capacity=10, product_id="1"),
    2: Pallet(2, 15, 15, 15, capacity=10, product_id="2"),
    3: Pallet(3, 20, 20, 20, capacity=10),  # Thêm pallet mới
    4: Pallet(4, 25, 25, 25, capacity=10),  # Thêm pallet mới
    5: Pallet(5, 30, 30, 30, capacity=10),  # Thêm pallet mới
    6: Pallet(6, 35, 35, 35, capacity=10),  # Thêm pallet mới
}

# Tối ưu hóa việc sắp xếp và lấy thông tin vị trí lưu trữ cho sản phẩm
# Tối ưu hóa việc sắp xếp và lấy thông tin vị trí lưu trữ cho sản phẩm
used_storage = optimize_storage(products, pallets)  # Change this line

# In ra vị trí lưu trữ của từng sản phẩm
for product, pallet in used_storage.items():
    print("Product {} ({}): Stored in pallet {}, Quantity: {}".format(product.name, product.id, pallet.id,
                                                                      product.quantity))
