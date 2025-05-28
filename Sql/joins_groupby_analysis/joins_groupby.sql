-- INNER JOIN: Customers with orders
SELECT c.name, c.city, o.order_id, o.amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- LEFT JOIN: All customers, even those with no orders
SELECT c.name, c.city, o.order_id, o.amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- RIGHT JOIN equivalent (not supported in SQLite, use LEFT JOIN from other side in practice)
-- For systems like PostgreSQL or MySQL:
SELECT o.order_id, o.amount, c.name, c.city
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;

-- GROUP BY city with total sales
SELECT c.city, SUM(o.amount) AS total_sales
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city;

-- GROUP BY with HAVING (only cities with sales > 10,000)
SELECT c.city, SUM(o.amount) AS total_sales
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
HAVING SUM(o.amount) > 10000;
