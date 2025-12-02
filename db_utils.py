from database.db_connect import get_db_connection

# ---------------------------------------------
# GENERIC QUERY EXECUTOR
# ---------------------------------------------
def execute(query, params=None, fetch=False):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(query, params or ())

    if fetch:
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    conn.commit()
    cursor.close()
    conn.close()
    return True


# ---------------------------------------------
# REGIONS
# ---------------------------------------------
def get_all_regions(search_query=None):
    if search_query:
        return execute(
            "SELECT * FROM Regions WHERE region_name LIKE %s OR region_code LIKE %s ORDER BY region_name",
            (f"%{search_query}%", f"%{search_query}%"),
            fetch=True
        )
    return execute(
        "SELECT * FROM Regions ORDER BY region_name",
        fetch=True
    )

def add_region(name, code):
    return execute(
        "INSERT INTO Regions (region_name, region_code) VALUES (%s, %s)",
        (name, code)
    )

def delete_region(id):
    return execute("DELETE FROM Regions WHERE id = %s", (id,))

def get_region_by_id(id):
    result = execute("SELECT * FROM Regions WHERE id = %s", (id,), fetch=True)
    return result[0] if result else None

def update_region(id, name, code):
    return execute(
        "UPDATE Regions SET region_name=%s, region_code=%s WHERE id=%s",
        (name, code, id)
    )


# ---------------------------------------------
# SOURCES
# ---------------------------------------------
def get_all_sources(search_query=None):
    if search_query:
        return execute(
            "SELECT * FROM Sources WHERE source_name LIKE %s OR source_organization LIKE %s ORDER BY source_name",
            (f"%{search_query}%", f"%{search_query}%"),
            fetch=True
        )
    return execute(
        "SELECT * FROM Sources ORDER BY source_name",
        fetch=True
    )

def add_source(name, org, url, desc):
    return execute(
        """
        INSERT INTO Sources (source_name, source_organization, source_url, description)
        VALUES (%s, %s, %s, %s)
        """,
        (name, org, url, desc)
    )

def get_source_by_id(id):
    result = execute("SELECT * FROM Sources WHERE id = %s", (id,), fetch=True)
    return result[0] if result else None

def update_source(id, name, org, url, desc):
    return execute(
        """
        UPDATE Sources 
        SET source_name=%s, source_organization=%s, source_url=%s, description=%s 
        WHERE id=%s
        """,
        (name, org, url, desc, id)
    )

def delete_source(id):
    return execute("DELETE FROM Sources WHERE id = %s", (id,))

# The following function is a duplicate and will be removed as per the instruction's implied removal.
# def delete_source(id):
#     return execute("DELETE FROM Sources WHERE id=%s", (id,))


# ---------------------------------------------
# CATEGORIES
# ---------------------------------------------
def get_all_categories():
    return execute(
        "SELECT * FROM IndicatorCategories ORDER BY category_name",
        fetch=True
    )

def add_category(name, desc):
    return execute(
        "INSERT INTO IndicatorCategories (category_name, description) VALUES (%s, %s)",
        (name, desc)
    )

def delete_category(id):
    return execute("DELETE FROM IndicatorCategories WHERE id=%s", (id,))


# ---------------------------------------------
# COUNTRIES
# ---------------------------------------------
# ---------------------------------------------
# COUNTRIES
# ---------------------------------------------
def get_all_countries(page=1, per_page=1000, search_query=None):
    offset = (page - 1) * per_page
    
    if search_query:
        count_query = """
            SELECT COUNT(*) as count 
            FROM Countries C
            LEFT JOIN Regions R ON C.region_id = R.id
            WHERE C.country_name LIKE %s OR C.country_code LIKE %s
        """
        count_result = execute(count_query, (f"%{search_query}%", f"%{search_query}%"), fetch=True)
        total_count = count_result[0]['count'] if count_result else 0
        
        items = execute(
            f"""
            SELECT C.*, R.region_name
            FROM Countries C
            LEFT JOIN Regions R ON C.region_id = R.id
            WHERE C.country_name LIKE %s OR C.country_code LIKE %s
            ORDER BY C.country_name
            LIMIT {per_page} OFFSET {offset}
            """,
            (f"%{search_query}%", f"%{search_query}%"),
            fetch=True
        )
    else:
        count_result = execute("SELECT COUNT(*) as count FROM Countries", fetch=True)
        total_count = count_result[0]['count'] if count_result else 0
        
        items = execute(
            f"""
            SELECT C.*, R.region_name
            FROM Countries C
            LEFT JOIN Regions R ON C.region_id = R.id
            ORDER BY C.country_name
            LIMIT {per_page} OFFSET {offset}
            """,
            fetch=True
        )
    return items, total_count

def get_country_by_code(code):
    result = execute(
        "SELECT * FROM Countries WHERE country_code=%s",
        (code,),
        fetch=True
    )
    return result[0] if result else None

def add_country(code, name, capital, region_id, income):
    return execute(
        """
        INSERT INTO Countries (country_code, country_name, capital_city, region_id, income_level)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (code, name, capital, region_id, income)
    )

def update_country(original_code, new_code, name, capital, region, income):
    return execute(
        """
        UPDATE Countries
        SET country_code=%s, country_name=%s, capital_city=%s,
            region_id=%s, income_level=%s
        WHERE country_code=%s
        """,
        (new_code, name, capital, region, income, original_code)
    )

def delete_country(code):
    return execute("DELETE FROM Countries WHERE country_code=%s", (code,))


# ---------------------------------------------
# INDICATORS
# ---------------------------------------------
def get_all_indicators(page=1, per_page=1000, search_query=None):
    offset = (page - 1) * per_page
    
    if search_query:
        count_query = """
            SELECT COUNT(*) as count 
            FROM Indicators I
            LEFT JOIN IndicatorCategories C ON I.category_id = C.id
            LEFT JOIN Sources S ON I.source_id = S.id
            WHERE I.indicator_name LIKE %s OR I.indicator_code LIKE %s
        """
        count_result = execute(count_query, (f"%{search_query}%", f"%{search_query}%"), fetch=True)
        total_count = count_result[0]['count'] if count_result else 0
        
        items = execute(
            f"""
            SELECT I.*, C.category_name, S.source_name
            FROM Indicators I
            LEFT JOIN IndicatorCategories C ON I.category_id = C.id
            LEFT JOIN Sources S ON I.source_id = S.id
            WHERE I.indicator_name LIKE %s OR I.indicator_code LIKE %s
            ORDER BY I.indicator_name
            LIMIT {per_page} OFFSET {offset}
            """,
            (f"%{search_query}%", f"%{search_query}%"),
            fetch=True
        )
    else:
        count_result = execute("SELECT COUNT(*) as count FROM Indicators", fetch=True)
        total_count = count_result[0]['count'] if count_result else 0
        
        items = execute(
            f"""
            SELECT I.*, C.category_name, S.source_name
            FROM Indicators I
            LEFT JOIN IndicatorCategories C ON I.category_id = C.id
            LEFT JOIN Sources S ON I.source_id = S.id
            ORDER BY I.indicator_name
            LIMIT {per_page} OFFSET {offset}
            """,
            fetch=True
        )
    return items, total_count

def get_indicators_by_category_name(category_name):
    return execute(
        """
        SELECT I.*, C.category_name, S.source_name
        FROM Indicators I
        LEFT JOIN IndicatorCategories C ON I.category_id = C.id
        LEFT JOIN Sources S ON I.source_id = S.id
        WHERE C.category_name LIKE %s
        ORDER BY I.indicator_name
        """,
        (f"%{category_name}%",),
        fetch=True
    )

def get_indicators_by_category_id(category_id, page=1, per_page=1000):
    offset = (page - 1) * per_page
    
    # Get total count
    count_result = execute("SELECT COUNT(*) as count FROM Indicators WHERE category_id = %s", (category_id,), fetch=True)
    total_count = count_result[0]['count'] if count_result else 0
    
    # Get paginated items
    items = execute(f"""
        SELECT i.*, s.source_name, c.category_name,
        EXISTS(SELECT 1 FROM IndicatorData d WHERE d.indicator_code = i.indicator_code) as has_data
        FROM Indicators i
        LEFT JOIN Sources s ON i.source_id = s.id
        LEFT JOIN IndicatorCategories c ON i.category_id = c.id
        WHERE i.category_id = %s
        ORDER BY has_data DESC, i.indicator_name ASC
        LIMIT {per_page} OFFSET {offset}
    """, (category_id,), fetch=True)
    
    return items, total_count

def add_indicator(code, name, source_id, category_id, definition):
    return execute(
        """
        INSERT INTO Indicators (indicator_code, indicator_name, source_id, category_id, long_definition)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (code, name, source_id, category_id, definition)
    )

def get_indicator_by_code(code):
    result = execute("SELECT * FROM Indicators WHERE indicator_code = %s", (code,), fetch=True)
    return result[0] if result else None

def update_indicator(code, name, source_id, category_id, definition):
    return execute(
        """
        UPDATE Indicators 
        SET indicator_name=%s, source_id=%s, category_id=%s, long_definition=%s 
        WHERE indicator_code=%s
        """,
        (name, source_id, category_id, definition, code)
    )

def delete_indicator(code):
    return execute("DELETE FROM Indicators WHERE indicator_code = %s", (code,))


# ---------------------------------------------
# INDICATOR DATA
# ---------------------------------------------
def get_data_by_country(code):
    return execute(
        """
        SELECT D.*, I.indicator_name
        FROM IndicatorData D
        JOIN Indicators I ON D.indicator_code = I.indicator_code
        WHERE D.country_code=%s
        ORDER BY D.year DESC
        """,
        (code,),
        fetch=True
    )

def get_data_by_composite_key(country_code, indicator_code, year):
    result = execute(
        """
        SELECT * FROM IndicatorData 
        WHERE country_code=%s AND indicator_code=%s AND year=%s
        """,
        (country_code, indicator_code, year),
        fetch=True
    )
    return result[0] if result else None

def add_indicator_data(country_code, indicator_code, year, value):
    return execute(
        """
        INSERT INTO IndicatorData (country_code, indicator_code, year, value)
        VALUES (%s, %s, %s, %s)
        """,
        (country_code, indicator_code, year, value)
    )

def update_indicator_data(country_code, indicator_code, year, value):
    return execute(
        """
        UPDATE IndicatorData 
        SET value=%s 
        WHERE country_code=%s AND indicator_code=%s AND year=%s
        """,
        (value, country_code, indicator_code, year)
    )

def delete_indicator_data(country_code, indicator_code, year):
    return execute(
        "DELETE FROM IndicatorData WHERE country_code=%s AND indicator_code=%s AND year=%s",
        (country_code, indicator_code, year)
    )

def add_indicator_data(country_code, indicator_code, year, value, footnote):
    return execute(
        """
        INSERT INTO IndicatorData (country_code, indicator_code, year, value, footnote)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (country_code, indicator_code, year, value, footnote)
    )

def delete_indicator_data(id):
    return execute("DELETE FROM IndicatorData WHERE id=%s", (id,))


# ---------------------------------------------
# DASHBOARD FUNCTIONS
# ---------------------------------------------
def get_yearly_indicator_average(indicator_code):
    return execute(
        """
        SELECT year, AVG(value) AS avg_value
        FROM IndicatorData
        WHERE indicator_code=%s
        GROUP BY year
        ORDER BY year
        """,
        (indicator_code,),
        fetch=True
    )

def get_global_population():
    return get_yearly_indicator_average("SP.POP.TOTL")

def get_global_gdp():
    return get_yearly_indicator_average("NY.GDP.MKTP.CD")

def get_global_life_expectancy():
    return get_yearly_indicator_average("SP.DYN.LE00.IN")

def get_chart_data(country_code, indicator_code, start_year=None, end_year=None):
    query = """
        SELECT year, value 
        FROM IndicatorData 
        WHERE country_code = %s AND indicator_code = %s
    """
    params = [country_code, indicator_code]
    
    if start_year:
        query += " AND year >= %s"
        params.append(start_year)
    
    if end_year:
        query += " AND year <= %s"
        params.append(end_year)
        
    query += " ORDER BY year ASC"
    
    return execute(query, tuple(params), fetch=True)

def get_recent_activity(limit=5):
    return execute(
        """
        SELECT D.year, D.value, C.country_name, I.indicator_name
        FROM IndicatorData D
        JOIN Countries C ON D.country_code = C.country_code
        JOIN Indicators I ON D.indicator_code = I.indicator_code
        ORDER BY D.id DESC
        LIMIT %s
        """,
        (limit,),
        fetch=True
    )

def get_latest_population_by_country():
    return execute(
        """
        SELECT C.country_name, D.value AS population, D.year
        FROM IndicatorData D
        JOIN Countries C ON C.country_code = D.country_code
        WHERE D.indicator_code='SP.POP.TOTL'
        AND D.year = (
            SELECT MAX(year)
            FROM IndicatorData
            WHERE country_code = D.country_code
            AND indicator_code='SP.POP.TOTL'
        )
        ORDER BY D.value DESC
        LIMIT 10
        """,
        fetch=True
    )
def get_health_indicators(page=1, per_page=1000, search_query=None):
    offset = (page - 1) * per_page
    
    if search_query:
        count_query = """
            SELECT COUNT(*) as count 
            FROM HealthIndicators i
            WHERE i.indicator_name LIKE %s OR i.indicator_code LIKE %s
        """
        count_result = execute(count_query, (f"%{search_query}%", f"%{search_query}%"), fetch=True)
        total_count = count_result[0]['count'] if count_result else 0
        
        items = execute(f"""
            SELECT i.*, s.source_name, c.category_name,
            EXISTS(SELECT 1 FROM IndicatorData d WHERE d.indicator_code = i.indicator_code) as has_data
            FROM HealthIndicators i
            LEFT JOIN Sources s ON i.source_id = s.id
            LEFT JOIN IndicatorCategories c ON i.category_id = c.id
            WHERE i.indicator_name LIKE %s OR i.indicator_code LIKE %s
            ORDER BY has_data DESC, i.indicator_name ASC
            LIMIT {per_page} OFFSET {offset}
        """, (f"%{search_query}%", f"%{search_query}%"), fetch=True)
    else:
        count_result = execute("SELECT COUNT(*) as count FROM HealthIndicators", fetch=True)
        total_count = count_result[0]['count'] if count_result else 0
        
        items = execute(f"""
            SELECT i.*, s.source_name, c.category_name,
            EXISTS(SELECT 1 FROM IndicatorData d WHERE d.indicator_code = i.indicator_code) as has_data
            FROM HealthIndicators i
            LEFT JOIN Sources s ON i.source_id = s.id
            LEFT JOIN IndicatorCategories c ON i.category_id = c.id
            ORDER BY has_data DESC, i.indicator_name ASC
            LIMIT {per_page} OFFSET {offset}
        """, fetch=True)
    
    return items, total_count

def get_economy_indicators(page=1, per_page=1000, search_query=None):
    offset = (page - 1) * per_page
    
    if search_query:
        count_query = """
            SELECT COUNT(*) as count 
            FROM EconomyIndicators i
            WHERE i.indicator_name LIKE %s OR i.indicator_code LIKE %s
        """
        count_result = execute(count_query, (f"%{search_query}%", f"%{search_query}%"), fetch=True)
        total_count = count_result[0]['count'] if count_result else 0
        
        items = execute(f"""
            SELECT i.*, s.source_name, c.category_name,
            EXISTS(SELECT 1 FROM IndicatorData d WHERE d.indicator_code = i.indicator_code) as has_data
            FROM EconomyIndicators i
            LEFT JOIN Sources s ON i.source_id = s.id
            LEFT JOIN IndicatorCategories c ON i.category_id = c.id
            WHERE i.indicator_name LIKE %s OR i.indicator_code LIKE %s
            ORDER BY has_data DESC, i.indicator_name ASC
            LIMIT {per_page} OFFSET {offset}
        """, (f"%{search_query}%", f"%{search_query}%"), fetch=True)
    else:
        count_result = execute("SELECT COUNT(*) as count FROM EconomyIndicators", fetch=True)
        total_count = count_result[0]['count'] if count_result else 0
        
        items = execute(f"""
            SELECT i.*, s.source_name, c.category_name,
            EXISTS(SELECT 1 FROM IndicatorData d WHERE d.indicator_code = i.indicator_code) as has_data
            FROM EconomyIndicators i
            LEFT JOIN Sources s ON i.source_id = s.id
            LEFT JOIN IndicatorCategories c ON i.category_id = c.id
            ORDER BY has_data DESC, i.indicator_name ASC
            LIMIT {per_page} OFFSET {offset}
        """, fetch=True)
    
    return items, total_count

def get_education_indicators(page=1, per_page=1000, search_query=None):
    offset = (page - 1) * per_page
    
    if search_query:
        count_query = """
            SELECT COUNT(*) as count 
            FROM EducationIndicators i
            WHERE i.indicator_name LIKE %s OR i.indicator_code LIKE %s
        """
        count_result = execute(count_query, (f"%{search_query}%", f"%{search_query}%"), fetch=True)
        total_count = count_result[0]['count'] if count_result else 0
        
        items = execute(f"""
            SELECT i.*, s.source_name, c.category_name,
            EXISTS(SELECT 1 FROM IndicatorData d WHERE d.indicator_code = i.indicator_code) as has_data
            FROM EducationIndicators i
            LEFT JOIN Sources s ON i.source_id = s.id
            LEFT JOIN IndicatorCategories c ON i.category_id = c.id
            WHERE i.indicator_name LIKE %s OR i.indicator_code LIKE %s
            ORDER BY has_data DESC, i.indicator_name ASC
            LIMIT {per_page} OFFSET {offset}
        """, (f"%{search_query}%", f"%{search_query}%"), fetch=True)
    else:
        count_result = execute("SELECT COUNT(*) as count FROM EducationIndicators", fetch=True)
        total_count = count_result[0]['count'] if count_result else 0
        
        items = execute(f"""
            SELECT i.*, s.source_name, c.category_name,
            EXISTS(SELECT 1 FROM IndicatorData d WHERE d.indicator_code = i.indicator_code) as has_data
            FROM EducationIndicators i
            LEFT JOIN Sources s ON i.source_id = s.id
            LEFT JOIN IndicatorCategories c ON i.category_id = c.id
            ORDER BY has_data DESC, i.indicator_name ASC
            LIMIT {per_page} OFFSET {offset}
        """, fetch=True)
    
    return items, total_count
# ---------------------------------------------
# CATEGORIES
# ---------------------------------------------
def get_all_categories(page=1, per_page=1000, search_query=None):
    offset = (page - 1) * per_page
    
    if search_query:
        count_result = execute(
            "SELECT COUNT(*) as count FROM IndicatorCategories WHERE category_name LIKE %s", 
            (f"%{search_query}%",), 
            fetch=True
        )
        total_count = count_result[0]['count'] if count_result else 0
        
        items = execute(
            f"""
            SELECT * FROM IndicatorCategories 
            WHERE category_name LIKE %s 
            ORDER BY category_name
            LIMIT {per_page} OFFSET {offset}
            """,
            (f"%{search_query}%",),
            fetch=True
        )
    else:
        count_result = execute("SELECT COUNT(*) as count FROM IndicatorCategories", fetch=True)
        total_count = count_result[0]['count'] if count_result else 0
        
        items = execute(
            f"""
            SELECT * FROM IndicatorCategories 
            ORDER BY category_name
            LIMIT {per_page} OFFSET {offset}
            """,
            fetch=True
        )
    return items, total_count

def add_category(name, description):
    return execute(
        "INSERT INTO IndicatorCategories (category_name, description) VALUES (%s, %s)",
        (name, description)
    )

def get_category_by_id(id):
    result = execute("SELECT * FROM IndicatorCategories WHERE id = %s", (id,), fetch=True)
    return result[0] if result else None

def update_category(id, name, description):
    return execute(
        "UPDATE IndicatorCategories SET category_name=%s, description=%s WHERE id=%s",
        (name, description, id)
    )

def delete_category(id):
    return execute("DELETE FROM IndicatorCategories WHERE id = %s", (id,))
