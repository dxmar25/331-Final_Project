import requests
import random
from datetime import datetime, timedelta

# Define the base URL of the REST API endpoint
base_url = "https://project-3-full-stack-agile-web-902-team-3-jctc.onrender.com/order/"


# Define the range of dates (two years ago to may)
start_date = (datetime.now() + timedelta(days=14)) - timedelta(days=730)
end_date = datetime.now() + timedelta(days=14)

# Define the start and end times for the hours of operation
start_hour = 9
end_hour = 22

# Initialize total sales counter and total revenue
total_sales = 0
total_revenue = 0.0

# Generate SQL for each day within the range
sql_queries = []
#start with semi full db
order_id = 41

while start_date <= end_date:
    # Generate a random number of orders for the current day
    num_orders = random.randint(50, 150)
    
    # Update total sales counter
    total_sales += num_orders
    
    # Calculate the time interval for each order within the day
    time_interval = (end_hour - start_hour) / num_orders
    
    # Generate orders with timestamps within the hours of operation for the current day
    for i in range(num_orders):
        # Generate random values for total, is_completed, and employee_id
        total = round(random.uniform(2.12, 55.99), 2)
        is_completed = 1
        employee_id = random.randint(1, 5)
        
        # Update total revenue
        total_revenue += total
        
        # Calculate the timestamp for the current order within the hours of operation
        hour = start_hour + int(i * time_interval)
        minute = random.randint(0, 59)
        
        # Create a datetime object for the timestamp
        timestamp = datetime(start_date.year, start_date.month, start_date.day, hour, minute)
        
        # Format the timestamp as a string
        timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        
        # Append the SQL query for the current order to the list
        #     {
        #     "id": 40,
        #     "total": 31.259999999999998,
        #     "timestamp": "2024-04-28T06:56:45.368000Z",
        #     "status": 0,
        #     "employee": 12
        # }
        #sql_queries.append(f"({order_id}, {total}, '{timestamp_str}', {is_completed}, {employee_id})")
        # Order.objects.create(
        #     id=order_id,
        #     total=total,
        #     timestamp=timestamp_str,
        #     status=is_completed,
        #     employee=employee_id
        # )
        
        # Define the data to be sent in the POST request
        data = {
            "id": order_id,
            "total": total,
            "timestamp": timestamp_str,
            "status": is_completed,
            "employee": employee_id
        }

        # Send a POST request to create a new entry
        response = requests.post(base_url, json=data)

        # Check if the request was successful (status code 201 indicates successful creation)
        if response.status_code == 201:
            print("New entry created successfully!")
            print("Response data:", response.json())
        else:
            print("Failed to create new entry. Status code:", response.status_code)
            print("Response:", response.text)

        order_id += 1
    
    # Move to the next day
    start_date += timedelta(days=1)

print("Total number of sales:", total_sales)
print("Total revenue:", round(total_revenue, 2))



