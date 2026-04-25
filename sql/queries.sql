-- Query 1: Total Revenue by Product Category
SELECT p.category,
       COUNT(*) AS num_orders,
       SUM(f.quantity) AS total_units,
       ROUND(SUM(f.amount_inr), 2) AS total_revenue_inr
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY total_revenue_inr DESC;


-- Query 2: Monthly Sales Trend
SELECT d.year, d.month, d.month_name,
       COUNT(*) AS orders,
       ROUND(SUM(f.amount_inr), 2) AS monthly_revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;


-- Query 3: Top 10 States by Revenue
SELECT l.state,
       COUNT(*) AS orders,
       ROUND(SUM(f.amount_inr), 2) AS revenue
FROM fact_sales f
JOIN dim_location l ON f.location_key = l.location_key
GROUP BY l.state
ORDER BY revenue DESC
LIMIT 10;


-- Query 4: Order Cancellation Rate by Category
SELECT p.category,
       COUNT(*) AS total_orders,
       SUM(CASE WHEN s.status_category = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
       ROUND(100.0 * SUM(CASE WHEN s.status_category = 'Cancelled'
             THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancel_rate_pct
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_order_status s ON f.status_key = s.status_key
GROUP BY p.category
ORDER BY cancel_rate_pct DESC;


-- Query 5: B2B vs B2C Revenue Comparison
SELECT
    CASE WHEN f.is_b2b THEN 'B2B' ELSE 'B2C' END AS customer_type,
    COUNT(*) AS orders,
    ROUND(SUM(f.amount_inr), 2) AS total_revenue
FROM fact_sales f
GROUP BY f.is_b2b;

