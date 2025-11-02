-- Insert into DataSources
INSERT INTO DataSources (id, source_name, source_url, description)
VALUES 
(1, 'World Development Indicators', 'https://databank.worldbank.org/source/world-development-indicators', 'Primary dataset from the World Bank.');

-- Insert into Regions
INSERT INTO Regions (id, source_id, region_name, income_group, world_bank_code)
VALUES
(1, 1, 'Europe & Central Asia', 'High income', 'ECS'),
(2, 1, 'Sub-Saharan Africa', 'Low income', 'SSF');

-- Insert into Countries
INSERT INTO Countries (id, region_id, country_name, country_code_alpha3, capital_city)
VALUES
(1, 1, 'Turkey', 'TUR', 'Ankara'),
(2, 1, 'Germany', 'DEU', 'Berlin'),
(3, 2, 'Nigeria', 'NGA', 'Abuja');

-- Insert into IndicatorCategories
INSERT INTO IndicatorCategories (id, source_id, category_name, description, topic)
VALUES
(1, 1, 'Economic Indicators', 'Indicators related to economy', 'Economy'),
(2, 1, 'Social Indicators', 'Indicators related to social development', 'Society');

-- Insert into Indicators
INSERT INTO Indicators (id, category_id, indicator_name, indicator_code, unit_of_measure)
VALUES
(1, 1, 'GDP per capita', 'NY.GDP.PCAP.CD', 'USD'),
(2, 2, 'Life expectancy at birth', 'SP.DYN.LE00.IN', 'Years'),
(3, 2, 'Internet users', 'IT.NET.USER.ZS', '% of population');

-- Insert into IndicatorData
INSERT INTO IndicatorData (indicator_id, country_id, year, value)
VALUES
(1, 1, 2020, 9534.75),
(1, 2, 2020, 47600.30),
(2, 1, 2020, 77.7),
(2, 3, 2020, 54.3),
(3, 1, 2020, 82.5),
(3, 2, 2020, 91.3);
