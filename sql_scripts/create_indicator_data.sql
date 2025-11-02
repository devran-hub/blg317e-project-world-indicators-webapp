CREATE TABLE IndicatorData (
    id SERIAL PRIMARY KEY,
    
    indicator_id INT NOT NULL,
    country_id INT NOT NULL,
    
    year INT NOT NULL,
    value NUMERIC,
    
    CONSTRAINT fk_indicator
        FOREIGN KEY(indicator_id)
        REFERENCES Indicators(id),
    CONSTRAINT fk_country
        FOREIGN KEY(country_id)
        REFERENCES Countries(id),
    CONSTRAINT uq_indicator_country_year
        UNIQUE (indicator_id, country_id, year)
);


