-- Rows where product line contains a substring (case-insensitive)
SELECT *
FROM supermarket_sales
WHERE product_line ILIKE '%Health and beauty%'
ORDER BY sale_date, sale_time;
