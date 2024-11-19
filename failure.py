from client import Client
from repo import Repo

if __name__ == "__main__":
    client = Client()

    print("Submitting tasks to the distributed task queue...")
    
    tasks = []
    for i in range(20):  # Increase the number of tasks as needed
        tasks.append({"task_type": "calculate_revenue", 
                      "args": {"data": {"Product_sold": [{"quantity": 10+i}]}}})
        tasks.append({"task_type": "calculate_commission", 
                      "args": {"data": {"Product_sold": [{"quantity": 15+i}]}}})
        tasks.append({"task_type": "calculate_loss", 
                      "args": {"data": {"Product_sold": [{"product_id": i}], 
                                        "Product_return": [{"product_id": i, "quantity": 3}]}}})

    task_ids = []
    for task in tasks:
        task_id = client.submit_task(task["task_type"], task["args"])
        # print(f"Submitted task ID: {task_id}")
        task_ids.append(task_id)


    print("\nAll submitted task IDs:")
    for idx, task_id in enumerate(task_ids):
        print(f"{idx + 1}. {task_id}")

    while True:
        repo = Repo()
        try:
            choice = int(input("\nEnter the number of the task ID to query its status (or 0 to exit): "))
            if choice == 0:
                print("Exiting...")
                break
            elif 1 <= choice <= len(task_ids):
                task_id = task_ids[choice - 1]
                status = repo.query_status(task_id)
                print(f"\nTask ID {task_id}\nStatus: {status[0]}")
                if status[0] == "Completed":
                    print(f"{status[1]} : {status[2]}")
            else:
                print("Invalid choice. Please select a valid task number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
