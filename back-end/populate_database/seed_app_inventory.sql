INSERT INTO app_inventory (id, name, price, stock, reorder_level) VALUES
-- All Specific Items for Burgers
(1, 'Beef Patty', 0.50, 1000, 50),
(2, 'American Cheese', 0.10, 1000, 50),
(3, 'Pickle', 0.02, 3000, 500),
(4, 'Lettuce', 0.05, 1000, 200),
(5, 'Tomato', 0.30, 500, 100),
(6, 'Onions', 0.30, 500, 100),
(7, 'Bacon', 0.15, 500, 50),
(8, 'Bun', 0.25, 1500, 100),
(9, 'Black Bean', 0.05, 1000, 100),

-- All specific items for Baskets
(10, 'Chicken Tender', 0.15, 800, 50),
(11, 'Texas Toast', 0.20, 500, 100),
(12, 'Gravy', 0.15, 750, 200),
(13, 'Steak Finger', 0.20, 1000, 100),

-- All specific items for Sandwiches
(14, 'American Swiss', 0.10, 1000, 50),
(15, 'Pepper Jack Cheese', 0.10, 1000, 50),
(16, 'Grilled Chicken', 0.50, 300, 50),

-- ALL Shakes and Sweets
(17, 'Cookie', 0.50, 300, 30),
(18, 'Brownie', 0.50, 300, 30),
(19, 'Chocolate Ice Cream', 0.15, 400, 50),
(20, 'Vanilla Ice Cream', 0.15, 400, 50),
(21, 'Cappuccino Ice Cream', 0.15, 400, 50),
(22, 'Milk', 0.15, 300, 50),
(23, 'Salad', 0.20, 400, 40),

-- All Beverages
(24, 'Reg Cup', 0.05, 1000, 200),
(25, 'Large Cup', 0.05, 1000, 200),
(26, 'Coffee', 0.02, 500, 100),

-- All Sides
(27, 'Fries', 0.15, 3000, 500),
(28, 'Tator Tots', 0.15, 2000, 300),
(29, 'Onion Rings', 0.15, 1500, 300),
(30, 'Kettle Chips', 0.25, 500, 100),

-- All Sauce
(31, 'Gig ''Em Sauce', 0.01, 2000, 200),
(32, 'Buffalo', 0.01, 2000, 200),
(33, 'Ranch', 0.01, 2000, 200),
(34, 'BBQ Sauce', 0.01, 2000, 200),
(35, 'Honey Mustard', 0.01, 2000, 200),
(36, 'Spicy Ranch', 0.01, 2000, 200),

-- All misk items
(37, 'Napkins', 0.05, 2000, 200),
(38, 'Straw', 0.02, 2000, 200)

ON CONFLICT(id)
DO UPDATE SET
    name = EXCLUDED.name,
    price = EXCLUDED.price,
    stock = EXCLUDED.stock,
    reorder_level = EXCLUDED.reorder_level;