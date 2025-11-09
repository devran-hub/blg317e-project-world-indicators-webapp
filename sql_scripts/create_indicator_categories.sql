CREATE TABLE IndicatorCategories (
    id SERIAL PRIMARY KEY,
    
    source_id INT,
    
    category_name VARCHAR(255) NOT NULL,
    description TEXT,
    topic VARCHAR(255),
    
    CONSTRAINT fk_source
        FOREIGN KEY(source_id) 
        REFERENCES DataSources(id)
);


