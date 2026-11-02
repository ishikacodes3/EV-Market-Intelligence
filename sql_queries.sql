-- Run these queries in DB Browser for SQLite or any SQLite client.
-- 1. Total sales by vehicle category
SELECT category, SUM(annual_sales) AS total_sales
FROM ev_vehicles GROUP BY category ORDER BY total_sales DESC;

-- 2. Manufacturer market share (share of sales represented in this dataset)
SELECT manufacturer, SUM(annual_sales) AS sales,
       ROUND(100.0 * SUM(annual_sales) / (SELECT SUM(annual_sales) FROM ev_vehicles), 2) AS market_share_pct
FROM ev_vehicles GROUP BY manufacturer ORDER BY sales DESC;

-- 3. Battery technology distribution
SELECT battery_technology, COUNT(*) AS model_records
FROM ev_vehicles GROUP BY battery_technology ORDER BY model_records DESC;

-- 4. Average driving range by category
SELECT category, ROUND(AVG(driving_range_km), 1) AS avg_range_km
FROM ev_vehicles GROUP BY category ORDER BY avg_range_km DESC;

-- 5. Manufacturing country summary
SELECT manufacturing_country, COUNT(*) AS records, SUM(annual_sales) AS sales
FROM ev_vehicles GROUP BY manufacturing_country ORDER BY sales DESC;

-- 6. Customer satisfaction by manufacturer
SELECT manufacturer, ROUND(AVG(customer_rating), 2) AS avg_rating
FROM ev_vehicles GROUP BY manufacturer ORDER BY avg_rating DESC;

-- 7. Outlier check using approximate IQR bounds for driving range
WITH quartiles AS (
  SELECT
    (SELECT driving_range_km FROM ev_vehicles ORDER BY driving_range_km LIMIT 1 OFFSET (SELECT CAST(COUNT(*)*0.25 AS INT) FROM ev_vehicles)) AS q1,
    (SELECT driving_range_km FROM ev_vehicles ORDER BY driving_range_km LIMIT 1 OFFSET (SELECT CAST(COUNT(*)*0.75 AS INT) FROM ev_vehicles)) AS q3
)
SELECT * FROM ev_vehicles, quartiles
WHERE driving_range_km < q1 - 1.5*(q3-q1) OR driving_range_km > q3 + 1.5*(q3-q1);
