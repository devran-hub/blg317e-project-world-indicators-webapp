-- Queries by Yunus Korkmaz (150220069)
-- Focus: Indicators, IndicatorCategories, IndicatorData
-- Param-style used: :indicator_code, :year, :country_code (adapt as needed)

-- 1) Top N countries by indicator and year
-- Returns top 10 by default; change LIMIT for different N
SELECT
  c.country_name,
  c.country_code_alpha3 AS country_code,
  idt.year,
  idt.value,
  i.indicator_name,
  i.indicator_code,
  ic.category_name
FROM IndicatorData idt
JOIN Indicators i ON i.id = idt.indicator_id
JOIN IndicatorCategories ic ON ic.id = i.category_id
JOIN Countries c ON c.id = idt.country_id
WHERE i.indicator_code = :indicator_code
  AND idt.year = :year
  AND idt.value IS NOT NULL
ORDER BY idt.value DESC
LIMIT 10;

-- 2) Time series for a country and indicator
SELECT
  idt.year,
  idt.value,
  c.country_name,
  c.country_code_alpha3 AS country_code,
  i.indicator_name,
  i.indicator_code
FROM IndicatorData idt
JOIN Indicators i ON i.id = idt.indicator_id
JOIN Countries c ON c.id = idt.country_id
WHERE i.indicator_code = :indicator_code
  AND c.country_code_alpha3 = :country_code
ORDER BY idt.year ASC;

-- 3) Regional average for an indicator and year
SELECT
  r.region_name,
  idt.year,
  AVG(idt.value) AS avg_value,
  i.indicator_name,
  i.indicator_code
FROM IndicatorData idt
JOIN Indicators i ON i.id = idt.indicator_id
JOIN Countries c ON c.id = idt.country_id
JOIN Regions r ON r.id = c.region_id
WHERE i.indicator_code = :indicator_code
  AND idt.year = :year
  AND idt.value IS NOT NULL
GROUP BY r.region_name, idt.year, i.indicator_name, i.indicator_code
ORDER BY avg_value DESC;

-- 4) Latest available value per country for an indicator
-- Uses window function to pick latest non-null year per country
WITH ranked AS (
  SELECT
    idt.country_id,
    idt.year,
    idt.value,
    ROW_NUMBER() OVER (PARTITION BY idt.country_id ORDER BY idt.year DESC) AS rn
  FROM IndicatorData idt
  JOIN Indicators i ON i.id = idt.indicator_id
  WHERE i.indicator_code = :indicator_code
    AND idt.value IS NOT NULL
)
SELECT
  c.country_name,
  c.country_code_alpha3 AS country_code,
  rgn.region_name,
  ranked.year,
  ranked.value
FROM ranked
JOIN Countries c ON c.id = ranked.country_id
JOIN Regions rgn ON rgn.id = c.region_id
WHERE ranked.rn = 1
ORDER BY ranked.value DESC;

-- 5) Category-level summary: average per indicator in a category for a year
SELECT
  ic.category_name,
  i.indicator_name,
  i.indicator_code,
  idt.year,
  AVG(idt.value) AS avg_value,
  COUNT(idt.value) AS country_count
FROM IndicatorData idt
JOIN Indicators i ON i.id = idt.indicator_id
JOIN IndicatorCategories ic ON ic.id = i.category_id
WHERE ic.category_name = :category_name
  AND idt.year = :year
  AND idt.value IS NOT NULL
GROUP BY ic.category_name, i.indicator_name, i.indicator_code, idt.year
ORDER BY avg_value DESC;


