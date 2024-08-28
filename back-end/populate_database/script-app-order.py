import random
from datetime import datetime, timedelta

# Define the range of dates (two years ago to today)
start_date = datetime.now() - timedelta(days=730)
end_date = datetime.now()

# Define the start and end times for the hours of operation
start_hour = 9
end_hour = 22

# Initialize total sales counter and total revenue
total_sales = 0
total_revenue = 0.0

# Generate SQL for each day within the range
sql_queries = []
order_id = 1

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
        is_completed = 'true'
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
        sql_queries.append(f"({order_id}, {total}, '{timestamp_str}', {is_completed}, {employee_id})")
        order_id += 1
    
    # Move to the next day
    start_date += timedelta(days=1)

# Combine all SQL queries into a single string
sql_query = "INSERT INTO app_order (id, total, timestamp, is_completed, employee_id) VALUES " + ",\n".join(sql_queries) + ";"

# Write the generated SQL query to a text file
with open('seed_app_order.sql', 'w') as file:
    file.write(sql_query)

# Print the total number of sales and total revenue
print("Total number of sales:", total_sales)
print("Total revenue:", round(total_revenue, 2))
