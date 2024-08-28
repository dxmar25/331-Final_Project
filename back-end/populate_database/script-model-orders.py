import os
import sys

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (project root) and append the 'app' directory to it
app_dir = os.path.join(current_dir, '..', 'app')

# Add the 'app' directory to the Python path
sys.path.append(app_dir)

from models.order import Order
import random
from datetime import datetime, timedelta

'''
    METHODS COPIED OVER FROM SCRIPT-APP-ORDER.PY
    TWEAKED TO WORK WITH DJANGO MODELS
'''

def seed_orders():
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
            Order.objects.create(
                id=order_id,
                total=total,
                timestamp=timestamp_str,
                status=is_completed,
                employee=employee_id
            )

            order_id += 1
        
        # Move to the next day
        start_date += timedelta(days=1)
    
    print("Total number of sales:", total_sales)
    print("Total revenue:", round(total_revenue, 2))



if __name__ == "__main__":
    seed_orders()