CREATE TABLE DataSources (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    source_name VARCHAR(255) NOT NULL, 
    description TEXT,                  
    url VARCHAR(2048)                  
) ENGINE=InnoDB;



CREATE TABLE IndicatorCategories (
    id INT PRIMARY KEY AUTO_INCREMENT, -- Primary Key
    source_id INT,                    -- Foreign Key
    category_name VARCHAR(255) NOT NULL,
    description TEXT,
    topic VARCHAR(100),

    
    CONSTRAINT FK_IndicatorCategories_DataSources
        FOREIGN KEY (source_id)
        REFERENCES DataSources(id)
        ON DELETE SET NULL 
) ENGINE=InnoDB;