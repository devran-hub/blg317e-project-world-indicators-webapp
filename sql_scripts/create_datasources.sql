CREATE TABLE DataSources (
    id SERIAL PRIMARY KEY,
    
    source_name VARCHAR(255) NOT NULL,
    source_url VARCHAR(512),
    description TEXT
);