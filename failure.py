from client import Client

if __name__ == "__main__":
    client = Client()

    print("Submitting tasks to the distributed task queue...")
    
    # Generate a large number of tasks
    tasks = []
    for i in range(20):  # Increase the number of tasks as needed
        tasks.append({"task_type": "calculate_revenue", 
                      "args": {"data": {"Product_sold": [{"quantity": 10+i}]}}})
        tasks.append({"task_type": "calculate_commission", 
                      "args": {"data": {"Product_sold": [{"quantity": 15+i}]}}})
        tasks.append({"task_type": "calculate_loss", 
                      "args": {"data": {"Product_sold": [{"product_id": i}], 
                                        "Product_return": [{"product_id": i, "quantity": 3}]}}})

    # Submit tasks and print their IDs
    task_ids = []
    for task in tasks:
        task_id = client.submit_task(task["task_type"], task["args"])
        print(f"Submitted task ID: {task_id}")
        task_ids.append(task_id)

    # Check task status examples
    print("\nChecking status for submitted tasks...")
    for task_id in task_ids:
        status = client.query_status(task_id)
        print(f"Task ID {task_id} status: {status}")
