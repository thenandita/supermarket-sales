/*

  Supermarket sales — sample SQL (PostgreSQL)

  Table name defaults to supermarket_sales (see db/.env TABLE_NAME).
  Full examples: queries-postgres.sql

*/

-- Inspect raw load
SELECT *
FROM supermarket_sales
LIMIT 25;

-- Total sales by city
SELECT city, SUM(sales) AS total_sales
FROM supermarket_sales
GROUP BY city
ORDER BY total_sales DESC;

-- Sales by product line
SELECT product_line, SUM(sales) AS total_sales, AVG(rating) AS avg_rating
FROM supermarket_sales
GROUP BY product_line
ORDER BY total_sales DESC;
