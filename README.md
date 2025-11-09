## blg317e-project-world-indicators-webapp

World Development Indicators-based database and SQL scripts for a web app that compares and visualizes development metrics across countries and time.

### Schema

- Main tables: `Regions`, `Countries`, `IndicatorCategories`, `Indicators`, `IndicatorData`
- Helper table: `DataSources`

### Setup (run in this order)

1. `sql_scripts/create_datasources.sql`
2. `sql_scripts/create_regions.sql`
3. `sql_scripts/create_countries.sql`
4. `sql_scripts/create_indicator_categories.sql`
5. `sql_scripts/create_indicators.sql`
6. `sql_scripts/create_indicator_data.sql`
7. `sql_scripts/insert_sample_data.sql`
8. (Optional) `sql_scripts/create_indexes_yunus.sql`

### Queries

- Member-specific queries:
  - `sql_scripts/queries_yunus.sql` (Indicators, IndicatorCategories, IndicatorData)
  - `sql_scripts/queries_mfatih.sql`
  - `sql_scripts/queries_ahmet.sql`
  - `sql_scripts/create_queries_fatih.sql`

Notes:

- Some queries use bind parameters like `:indicator_code`, `:year`, `:country_code`. Replace with your SQL client's parameter syntax as needed.
