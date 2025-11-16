DROP TABLE IF EXISTS Indicators;

CREATE TABLE Indicators (
    id SERIAL PRIMARY KEY,

    indicator_code VARCHAR(100) UNIQUE NOT NULL,
    indicator_name VARCHAR(255) NOT NULL,
    unit_of_measure VARCHAR(100),

    category_id INT REFERENCES IndicatorCategories(id),
    source_id INT REFERENCES DataSources(id)
);
