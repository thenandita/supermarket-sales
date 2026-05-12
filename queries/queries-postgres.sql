/*

  Supermarket sales — PostgreSQL analysis queries

  Assumes table supermarket_sales (see db/.env TABLE_NAME) loaded from
  data/supermarket-analysis.xlsx sheet "SuperMarket Analysis".

*/

--------------------------------------------------------------------------------------------------------------------------

-- 1. Preview

SELECT *
FROM supermarket_sales
ORDER BY sale_date, sale_time
LIMIT 50;

--------------------------------------------------------------------------------------------------------------------------

-- 2. Revenue by branch and city

SELECT branch, city, SUM(sales) AS total_sales, COUNT(*) AS transactions
FROM supermarket_sales
GROUP BY branch, city
ORDER BY total_sales DESC;

--------------------------------------------------------------------------------------------------------------------------

-- 3. Member vs normal customers

SELECT customer_type, SUM(sales) AS total_sales, AVG(sales) AS avg_ticket
FROM supermarket_sales
GROUP BY customer_type;

--------------------------------------------------------------------------------------------------------------------------

-- 4. Top product lines by revenue

SELECT product_line, SUM(sales) AS total_sales, SUM(quantity) AS units_sold
FROM supermarket_sales
GROUP BY product_line
ORDER BY total_sales DESC;

--------------------------------------------------------------------------------------------------------------------------

-- 5. Payment method mix

SELECT payment, COUNT(*) AS n, SUM(sales) AS total_sales
FROM supermarket_sales
GROUP BY payment
ORDER BY total_sales DESC;

--------------------------------------------------------------------------------------------------------------------------

-- 6. Monthly sales (from sale_date)

SELECT date_trunc('month', sale_date)::date AS month, SUM(sales) AS total_sales
FROM supermarket_sales
WHERE sale_date IS NOT NULL
GROUP BY 1
ORDER BY 1;

--------------------------------------------------------------------------------------------------------------------------

-- 7. Average rating by branch

SELECT branch, ROUND(AVG(rating)::numeric, 2) AS avg_rating, COUNT(*) AS n
FROM supermarket_sales
GROUP BY branch
ORDER BY avg_rating DESC;

--------------------------------------------------------------------------------------------------------------------------

-- 8. Duplicate invoice check (expect zero rows if data is clean)

SELECT invoice_id, COUNT(*) AS n
FROM supermarket_sales
GROUP BY invoice_id
HAVING COUNT(*) > 1;

--------------------------------------------------------------------------------------------------------------------------

-- 9. Gross margin summary

SELECT
  ROUND(SUM(gross_income)::numeric, 2) AS total_gross_income,
  ROUND(AVG(gross_margin_percentage)::numeric, 4) AS avg_margin_pct
FROM supermarket_sales;
