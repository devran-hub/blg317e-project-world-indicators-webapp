CREATE TABLE Indicators (
    id SERIAL PRIMARY KEY,
    
    category_id INT,
    
    indicator_name VARCHAR(255) NOT NULL,
    indicator_code VARCHAR(100) UNIQUE,
    unit_of_measure VARCHAR(100),
    
    CONSTRAINT fk_category
        FOREIGN KEY(category_id)
        REFERENCES IndicatorCategories(id)
);


