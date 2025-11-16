DROP TABLE IF EXISTS Regions;

CREATE TABLE Regions (
    id SERIAL PRIMARY KEY,
    region_name VARCHAR(255) NOT NULL,
    income_group VARCHAR(255),
    world_bank_code VARCHAR(50)
);
