import pandas as pd
import itertools

# Load the CSV file
file_path = './df_results.csv'
df = pd.read_csv(file_path)

# Inspect the dataframe to understand its structure
print(df.head())

# Assuming the CSV has columns: 'order_id' and 'item_position'
# Convert the dataframe into the orders dictionary
orders = {}
for _, row in df.iterrows():
    order_id = row['order_id']
    item_position = row['item_position']
    if order_id not in orders:
        orders[order_id] = []
    orders[order_id].append(item_position)

# Print the orders dictionary to verify
print(orders)

# Batch capacity
batch_capacity = 2


# Function to calculate distance (simple Euclidean distance for demonstration)
def calculate_distance(positions):
    return sum(abs(positions[i] - positions[i + 1]) for i in range(len(positions) - 1))


# Function to create batches
def create_batches(orders, batch_capacity):
    order_keys = list(orders.keys())
    all_batches = []
    min_distance = float('inf')
    best_batch_combination = None

    # Try all possible batch combinations
    for combination in itertools.combinations(order_keys, batch_capacity):
        remaining_orders = list(set(order_keys) - set(combination))
        current_batches = [combination]

        # Create subsequent batches from remaining orders
        while remaining_orders:
            next_batch = remaining_orders[:batch_capacity]
            remaining_orders = remaining_orders[batch_capacity:]
            current_batches.append(next_batch)

        # Calculate total distance for current batch combination
        total_distance = sum(
            calculate_distance([item for order in batch for item in orders[order]]) for batch in current_batches)

        if total_distance < min_distance:
            min_distance = total_distance
            best_batch_combination = current_batches

    return best_batch_combination, min_distance


# Create and display optimal batches
optimal_batches, minimal_distance = create_batches(orders, batch_capacity)
print("Optimal Batches:", optimal_batches)
print("Minimal Total Distance:", minimal_distance)
