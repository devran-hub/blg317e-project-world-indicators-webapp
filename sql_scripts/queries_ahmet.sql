------------------------------------------------------------
-- 1. Average GDP per capita by region in 2020
------------------------------------------------------------
SELECT 
    r.region_name, 
    ROUND(AVG(idata.value), 2) AS avg_gdp_per_capita
FROM IndicatorData idata
JOIN Indicators i ON idata.indicator_id = i.id
JOIN Countries c ON idata.country_id = c.id
JOIN Regions r ON c.region_id = r.id
WHERE i.indicator_name = 'GDP per capita' 
  AND idata.year = 2020
GROUP BY r.region_name
ORDER BY avg_gdp_per_capita DESC;

------------------------------------------------------------
-- 2. Country with the highest Life Expectancy per region
------------------------------------------------------------
SELECT 
    r.region_name,
    c.country_name,
    idata.value AS life_expectancy
FROM IndicatorData idata
JOIN Indicators i ON idata.indicator_id = i.id
JOIN Countries c ON idata.country_id = c.id
JOIN Regions r ON c.region_id = r.id
WHERE i.indicator_name = 'Life expectancy at birth'
  AND idata.value = (
        SELECT MAX(id2.value)
        FROM IndicatorData id2
        JOIN Countries c2 ON id2.country_id = c2.id
        WHERE c2.region_id = r.id 
          AND id2.indicator_id = i.id
  )
ORDER BY r.region_name;

------------------------------------------------------------
-- 3. Internet usage growth by country (2015–2020)
------------------------------------------------------------
SELECT 
    c.country_name,
    (MAX(idata.value) - MIN(idata.value)) AS growth_percent
FROM IndicatorData idata
JOIN Indicators i ON idata.indicator_id = i.id
JOIN Countries c ON idata.country_id = c.id
WHERE i.indicator_name = 'Internet users'
  AND idata.year BETWEEN 2015 AND 2020
GROUP BY c.country_name
ORDER BY growth_percent DESC;
