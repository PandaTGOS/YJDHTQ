from consumer import Worker
import time

# Define task functions
def calculate_revenue(data):
    """
    Calculate total revenue from the given sales data.
    """
    total_revenue = 0
    for product in data["Product_sold"]:
        quantity = product["quantity"]
        cost_per_unit = product["cost_per_unit"]
        total_revenue += quantity * cost_per_unit
    
    time.sleep(2)
    return total_revenue

def calculate_commission(data, commission_rate=0.10):
    """
    Calculate commission based on the total revenue.
    Default commission rate is 10%.
    """
    total_revenue = calculate_revenue(data)
    commission = total_revenue * commission_rate
    time.sleep(2)
    return commission

def calculate_loss(data):
    """
    Calculate loss based on returned products.
    """
    total_loss = 0
    product_cost_map = {p["product_id"]: p["cost_per_unit"] for p in data["Product_sold"]}

    for returned_product in data.get("Product_return", []):
        product_id = returned_product["product_id"]
        quantity_returned = returned_product["quantity"]
        cost_per_unit = product_cost_map.get(product_id, 0)
        total_loss += quantity_returned * cost_per_unit
    time.sleep(2)
    return total_loss



worker = Worker()

# Register task functions
worker.run(calculate_revenue)
worker.run(calculate_commission)
worker.run(calculate_loss)

# Start the worker
worker.start_worker()