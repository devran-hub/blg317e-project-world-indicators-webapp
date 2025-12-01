CREATE DATABASE wdi;
USE wdi;

CREATE TABLE Regions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    region_name VARCHAR(100),
    region_code VARCHAR(20)
);

CREATE TABLE Countries (
    country_code CHAR(3) PRIMARY KEY,
    country_name VARCHAR(100),
    capital_city VARCHAR(100),
    region_id INT,
    income_level VARCHAR(100),

    FOREIGN KEY (region_id) REFERENCES Regions(id)
);

CREATE TABLE IndicatorCategories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(150),
    topic VARCHAR(150),
    description TEXT
);

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

CREATE TABLE IndicatorData (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_code CHAR(3),
    indicator_code VARCHAR(50),
    year INT,
    value DOUBLE,
    footnote TEXT,

    FOREIGN KEY (country_code) REFERENCES Countries(country_code),
    FOREIGN KEY (indicator_code) REFERENCES Indicators(indicator_code)
);


CREATE TABLE Sources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_name VARCHAR(150),
    source_organization VARCHAR(200),
    source_url VARCHAR(300),
    description TEXT
);


CREATE TABLE HealthIndicators (
    id INT AUTO_INCREMENT PRIMARY KEY,
    indicator_code VARCHAR(50) UNIQUE,
    indicator_name VARCHAR(255),
    long_definition TEXT,
    unit_of_measure VARCHAR(100),
    
    source_id INT,
    category_id INT,

    FOREIGN KEY (source_id) REFERENCES Sources(id),
    FOREIGN KEY (category_id) REFERENCES IndicatorCategories(id)
);


CREATE TABLE EconomyIndicators (
    id INT AUTO_INCREMENT PRIMARY KEY,
    indicator_code VARCHAR(50) UNIQUE,
    indicator_name VARCHAR(255),
    long_definition TEXT,
    unit_of_measure VARCHAR(100),
    
    source_id INT,
    category_id INT,

    FOREIGN KEY (source_id) REFERENCES Sources(id),
    FOREIGN KEY (category_id) REFERENCES IndicatorCategories(id)
);


CREATE TABLE EducationIndicators (
    id INT AUTO_INCREMENT PRIMARY KEY,
    indicator_code VARCHAR(50) UNIQUE,
    indicator_name VARCHAR(255),
    long_definition TEXT,
    unit_of_measure VARCHAR(100),
    
    source_id INT,
    category_id INT,

    FOREIGN KEY (source_id) REFERENCES Sources(id),
    FOREIGN KEY (category_id) REFERENCES IndicatorCategories(id)
);

SELECT indicator_code, indicator_name
FROM Indicators
WHERE indicator_name LIKE '%school%'
   OR indicator_name LIKE '%education%'
   OR indicator_name LIKE '%literacy%'
   OR indicator_name LIKE '%enrollment%'
   OR indicator_name LIKE '%teacher%'
   OR indicator_name LIKE '%student%'
LIMIT 200;

TRUNCATE TABLE EducationIndicators;

INSERT INTO EducationIndicators (indicator_code, indicator_name, long_definition, unit_of_measure, source_id, category_id)
SELECT indicator_code, indicator_name, long_definition, unit_of_measure, source_id, category_id
FROM Indicators
WHERE indicator_name LIKE '%school%'
   OR indicator_name LIKE '%education%'
   OR indicator_name LIKE '%literacy%'
   OR indicator_name LIKE '%enrollment%'
   OR indicator_name LIKE '%teacher%'
   OR indicator_name LIKE '%proficiency%'
   OR indicator_name LIKE '%student%'
   OR indicator_name LIKE '%classroom%'
   OR indicator_name LIKE '%youth%';


INSERT INTO HealthIndicators (indicator_code, indicator_name, long_definition, unit_of_measure, source_id, category_id)
SELECT indicator_code, indicator_name, long_definition, unit_of_measure, source_id, category_id
FROM Indicators
WHERE indicator_name LIKE '%health%'
   OR indicator_name LIKE '%mortality%'
   OR indicator_name LIKE '%death%'
   OR indicator_name LIKE '%birth%'
   OR indicator_name LIKE '%life expectancy%'
   OR indicator_name LIKE '%disease%'
   OR indicator_name LIKE '%nutrition%'
   OR indicator_name LIKE '%immunization%'
   OR indicator_name LIKE '%hospital%'
   OR indicator_name LIKE '%child%'
   OR indicator_name LIKE '%infant%'
   OR indicator_name LIKE '%HIV%'
   OR indicator_name LIKE '%TB%'
   OR indicator_name LIKE '%fertility%';

INSERT INTO EconomyIndicators (indicator_code, indicator_name, long_definition, unit_of_measure, source_id, category_id)
SELECT indicator_code, indicator_name, long_definition, unit_of_measure, source_id, category_id
FROM Indicators
WHERE indicator_name LIKE '%gdp%'
   OR indicator_name LIKE '%gni%'
   OR indicator_name LIKE '%income%'
   OR indicator_name LIKE '%inflation%'
   OR indicator_name LIKE '%price%'
   OR indicator_name LIKE '%market%'
   OR indicator_name LIKE '%trade%'
   OR indicator_name LIKE '%export%'
   OR indicator_name LIKE '%import%'
   OR indicator_name LIKE '%balance%'
   OR indicator_name LIKE '%fiscal%'
   OR indicator_name LIKE '%labor%'
   OR indicator_name LIKE '%employment%'
   OR indicator_name LIKE '%tax%'
   OR indicator_name LIKE '%consumption%'
   OR indicator_name LIKE '%production%'
   OR indicator_name LIKE '%investment%'
   OR indicator_name LIKE '%industry%'
   OR indicator_name LIKE '%debt%'
   OR indicator_name LIKE '%revenue%'
   OR indicator_name LIKE '%expenditure%';

INSERT INTO IndicatorCategories (category_name, description)
VALUES ('Health (Auto)', 'Automatically assigned health indicators without an official category');

UPDATE HealthIndicators
SET category_id = 24
WHERE category_id IS NULL;

SELECT COUNT(*) FROM EducationIndicators WHERE category_id IS NULL;
SELECT COUNT(*) FROM EconomyIndicators WHERE category_id IS NULL;

UPDATE EducationIndicators
SET category_id = 4
WHERE category_id IS NULL;

UPDATE EconomyIndicators
SET category_id = 3
WHERE category_id IS NULL;



SELECT id FROM IndicatorCategories WHERE category_name LIKE '%Health%';


SELECT id FROM IndicatorCategories WHERE category_name LIKE '%Education%';

SELECT id FROM IndicatorCategories WHERE category_name LIKE '%Economy%';


SHOW TABLES;










