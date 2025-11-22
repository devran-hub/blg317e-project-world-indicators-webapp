DROP TABLE IF EXISTS IndicatorData;
DROP TABLE IF EXISTS Indicators;
DROP TABLE IF EXISTS IndicatorCategories;
DROP TABLE IF EXISTS Sources;
DROP TABLE IF EXISTS Countries;
DROP TABLE IF EXISTS Regions;

-- 1) Regions Table
CREATE TABLE Regions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    region_code VARCHAR(20),
    region_name VARCHAR(150),
    admin_region VARCHAR(150),
    income_level VARCHAR(100),
    special_notes TEXT
);

-- 2) Countries Table
CREATE TABLE Countries (
    country_code VARCHAR(3) PRIMARY KEY,
    country_name VARCHAR(255),
    capital_city VARCHAR(255),
    region_id INT,
    income_level VARCHAR(100),
    FOREIGN KEY (region_id) REFERENCES Regions(id)
);

-- 3) IndicatorCategories Table
CREATE TABLE IndicatorCategories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255),
    source_note TEXT
);

-- 4) Sources Table
CREATE TABLE Sources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_name VARCHAR(255),
    organization VARCHAR(255),
    source_note TEXT,
    url TEXT
);

-- 5) Indicators Table
CREATE TABLE Indicators (
    indicator_code VARCHAR(50) PRIMARY KEY,
    indicator_name VARCHAR(255),
    long_definition TEXT,
    unit_of_measure VARCHAR(100),
    category_id INT,
    source_id INT,
    FOREIGN KEY (category_id) REFERENCES IndicatorCategories(id),
    FOREIGN KEY (source_id) REFERENCES Sources(id)
);

-- 6) IndicatorData Table
CREATE TABLE IndicatorData (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_code VARCHAR(3),
    indicator_code VARCHAR(50),
    year INT,
    value DOUBLE,
    footnote TEXT,
    FOREIGN KEY (country_code) REFERENCES Countries(country_code),
    FOREIGN KEY (indicator_code) REFERENCES Indicators(indicator_code)
);
