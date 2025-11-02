CREATE TABLE Regions (
    id SERIAL PRIMARY KEY,
    
    source_id INT,
    
    region_name VARCHAR(255) NOT NULL,
    income_group VARCHAR(255),
    world_bank_code VARCHAR(100) UNIQUE,
    
    CONSTRAINT fk_source
        FOREIGN KEY(source_id) 
        REFERENCES DataSources(id)
);