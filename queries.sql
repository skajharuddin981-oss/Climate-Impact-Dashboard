-- Live Climate Impact Dashboard: SQL

-- 1. Database and table
CREATE DATABASE climate_dashboard;
USE climate_dashboard;

CREATE TABLE air_quality_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(80),
    station_name VARCHAR(150),
    aqi INT,
    pm25 FLOAT,
    pm10 FLOAT,
    no2 FLOAT,
    so2 FLOAT,
    co FLOAT,
    o3 FLOAT,
    latitude FLOAT,
    longitude FLOAT,
    recorded_at VARCHAR(30),
    collected_at DATETIME
);

-- 2. Quick checks
SELECT * FROM air_quality_readings;
SELECT COUNT(*) FROM air_quality_readings;

-- 3. Analysis queries (run these and check the results against your data)

-- Average AQI per city, worst first
SELECT city, ROUND(AVG(aqi), 1) AS avg_aqi, COUNT(*) AS readings
FROM air_quality_readings
GROUP BY city
ORDER BY avg_aqi DESC;

-- AQI category distribution
SELECT
    CASE
        WHEN aqi <= 50  THEN 'Good'
        WHEN aqi <= 100 THEN 'Moderate'
        WHEN aqi <= 150 THEN 'Unhealthy for Sensitive Groups'
        WHEN aqi <= 200 THEN 'Unhealthy'
        WHEN aqi <= 300 THEN 'Very Unhealthy'
        ELSE 'Hazardous'
    END AS aqi_category,
    COUNT(*) AS readings
FROM air_quality_readings
GROUP BY aqi_category
ORDER BY readings DESC;

-- Daily trend per city
SELECT city, DATE(collected_at) AS day, ROUND(AVG(aqi), 1) AS avg_aqi
FROM air_quality_readings
GROUP BY city, DATE(collected_at)
ORDER BY day, city;

-- Most recent reading for each city (window function)
SELECT city, aqi, pm25, pm10, collected_at
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY city ORDER BY collected_at DESC) AS rn
    FROM air_quality_readings
) t
WHERE rn = 1;
