------------------------------------------------------------------
-- 1. Average indicator value per category (2020)
------------------------------------------------------------------
SELECT
    ic.category_name,
    ic.topic,
    ROUND(AVG(idata.value), 2) AS avg_indicator_value
FROM
    IndicatorCategories ic
JOIN
    Indicators i ON ic.id = i.category_id
JOIN
    IndicatorData idata ON i.id = idata.indicator_id
WHERE
    idata.year = 2020
GROUP BY
    ic.category_name, ic.topic
ORDER BY
    avg_indicator_value DESC;


------------------------------------------------------------------
-- 2. Indicator with the highest average value per category
------------------------------------------------------------------
WITH IndicatorAverages AS (
    -- calculate the average 
    SELECT
        i.id AS indicator_id,
        i.indicator_name,
        i.category_id,
        AVG(idata.value) AS avg_value
    FROM
        Indicators i
    JOIN
        IndicatorData idata ON i.id = idata.indicator_id
    GROUP BY
        i.id, i.indicator_name, i.category_id
),
RankedIndicators AS (
    
    SELECT
        ia.indicator_name,
        ic.category_name,
        ia.avg_value,
        ROW_NUMBER() OVER(
            PARTITION BY ic.category_name
            ORDER BY ia.avg_value DESC
        ) as rn
    FROM
        IndicatorAverages ia
    JOIN
        IndicatorCategories ic ON ia.category_id = ic.id
)
-- select the #1 ranked 
SELECT
    category_name,
    indicator_name,
    ROUND(avg_value, 2) AS highest_avg_value
FROM
    RankedIndicators
WHERE
    rn = 1;


------------------------------------------------------------------
-- 3. Average indicator growth by category (2015 vs 2020)
------------------------------------------------------------------
WITH YearValues AS (
    
    SELECT
        i.category_id,
        idata.indicator_id,
        MAX(CASE WHEN idata.year = 2015 THEN idata.value ELSE NULL END) AS val_2015,
        MAX(CASE WHEN idata.year = 2020 THEN idata.value ELSE NULL END) AS val_2020
    FROM
        IndicatorData idata
    JOIN
        Indicators i ON idata.indicator_id = i.id
    WHERE
        idata.year IN (2015, 2020)
    GROUP BY
        i.category_id, idata.indicator_id
),
IndicatorGrowth AS (
    
    SELECT
        category_id,
        (val_2020 - val_2015) AS growth
    FROM
        YearValues
    WHERE
        val_2015 IS NOT NULL AND val_2020 IS NOT NULL
)
-- average 
SELECT
    ic.category_name,
    ROUND(AVG(ig.growth), 2) AS avg_growth_2015_2020
FROM
    IndicatorGrowth ig
JOIN
    IndicatorCategories ic ON ig.category_id = ic.id
GROUP BY
    ic.category_name
ORDER BY
    avg_growth_2015_2020 DESC;