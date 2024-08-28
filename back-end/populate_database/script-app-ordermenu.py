# INSERT INTO app_ordermenu (id, quantity, menu_id, order_id) VALUES
# (1 to n iterations, random number from 1 to 3, random number from 1 to 47, 1-72812),

# order_id stays constant for the order as it should have random number of 1 to 5 items in it. for example
# (44, 1, 33, 15),
# (45, 2, 44, 15),
# (46, 1, 2, 15),
# (47, 1, 3, 15),
# (48, 2, 10, 16),

# And so on until order_id reaches 72812


import random

# Define the maximum order ID
max_order_id = 72812

# Initialize an empty list to store SQL queries
sql_queries = []

# Initialize the starting ID
current_id = 1

# Generate SQL queries for each order ID
for order_id in range(1, max_order_id + 1):
    # Generate a random number of items in the order (between 1 and 5)
    num_items = random.randint(1, 5)
    
    # Generate SQL queries for each item in the order
    for i in range(1, num_items + 1):
        # Generate a random quantity for the item (between 1 and 3)
        quantity = random.randint(1, 3)
        
        # Generate a random menu ID for the item (between 1 and 47)
        menu_id = random.randint(1, 47)
        
        # Append the SQL query for the current item to the list
        sql_queries.append(f"({current_id}, {quantity}, {menu_id}, {order_id})")
        
        # Increment the ID for the next item
        current_id += 1

# Combine all SQL queries into a single string
sql_query = "INSERT INTO app_ordermenu (id, quantity, menu_id, order_id) VALUES " + ",\n".join(sql_queries) + ";"

# Write the generated SQL query to a text file
with open('seed_app_ordermenu.sql', 'w') as file:
    file.write(sql_query)
