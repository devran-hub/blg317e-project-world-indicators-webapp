CREATE TABLE Countries (
    id SERIAL PRIMARY KEY,
    region_id INT,
    country_name VARCHAR(255) NOT NULL,
    country_code_alpha3 CHAR(3) UNIQUE,
    capital_city VARCHAR(255),

    CONSTRAINT fk_region
        FOREIGN KEY(region_id)
        REFERENCES Regions(id)
);
