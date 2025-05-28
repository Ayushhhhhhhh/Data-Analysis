-- Create customers table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name TEXT,
    city TEXT
);

-- Insert customer data
INSERT INTO customers (customer_id, name, city) VALUES
(1, 'Riya', 'Delhi'),
(2, 'Aman', 'Mumbai'),
(3, 'Nita', 'Jaipur');

-- Create orders table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    amount INT,
    order_date DATE
);

-- Insert order data
INSERT INTO orders (order_id, customer_id, amount, order_date) VALUES
(101, 1, 5000, '2024-01-01'),
(102, 2, 6000, '2024-01-02'),
(103, 1, 7000, '2024-01-03');
