-- Indexes by Yunus Korkmaz (150220069)
-- These indexes improve common query patterns on IndicatorData and lookup by codes.

-- Fast filtering by indicator and year (time series, top N by year)
CREATE INDEX IF NOT EXISTS idx_indicator_data_indicator_year
  ON IndicatorData (indicator_id, year);

-- Fast filtering by country and year (country trend queries)
CREATE INDEX IF NOT EXISTS idx_indicator_data_country_year
  ON IndicatorData (country_id, year);

-- Lookup indicators by code
CREATE INDEX IF NOT EXISTS idx_indicators_indicator_code
  ON Indicators (indicator_code);

-- Category name lookups
CREATE INDEX IF NOT EXISTS idx_indicator_categories_category_name
  ON IndicatorCategories (category_name);


