import mysql.connector
from database.db_connect import get_connection

# Helper Function (Wrapper)

def execute_query(query, params=None, fetch=False):

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True) 
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
            return True
            
    except mysql.connector.Error as e:
        print(f"VERİTABANI HATASI: {e}")
        print(f"Hatalı Sorgu: {query}")
        if conn:
            conn.rollback() 
        return None if fetch else False
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# -------------------------------------------------------------------
# Regions Table
# -------------------------------------------------------------------

def get_all_regions():
    return execute_query("SELECT * FROM Regions ORDER BY region_name", fetch=True)

def add_region(name, code):
    sql = "INSERT INTO Regions (region_name, region_code) VALUES (%s, %s)"
    return execute_query(sql, (name, code))

def update_region(id, name, code):
    sql = "UPDATE Regions SET region_name=%s, region_code=%s WHERE id=%s"
    return execute_query(sql, (name, code, id))

def delete_region(id):
    # Careful if there is a country that has this regions as FK
    sql = "DELETE FROM Regions WHERE id=%s"
    return execute_query(sql, (id,))

# -------------------------------------------------------------------
# Sources Table
# -------------------------------------------------------------------

def get_all_sources():
    return execute_query("SELECT * FROM Sources ORDER BY source_name", fetch=True)

def add_source(name, organization, url, description):
    sql = """
    INSERT INTO Sources (source_name, source_organization, source_url, description) 
    VALUES (%s, %s, %s, %s)
    """
    return execute_query(sql, (name, organization, url, description))

def update_source(id, name, organization, url, description):
    sql = """
    UPDATE Sources 
    SET source_name=%s, source_organization=%s, source_url=%s, description=%s 
    WHERE id=%s
    """
    return execute_query(sql, (name, organization, url, description, id))

def delete_source(id):
    return execute_query("DELETE FROM Sources WHERE id=%s", (id,))

# -------------------------------------------------------------------
# IndicatorCategories table
# -------------------------------------------------------------------

def get_all_categories():
    return execute_query("SELECT * FROM IndicatorCategories ORDER BY category_name", fetch=True)

def add_category(name, description):
    sql = "INSERT INTO IndicatorCategories (category_name, description) VALUES (%s, %s)"
    return execute_query(sql, (name, description))

def delete_category(id):
    return execute_query("DELETE FROM IndicatorCategories WHERE id=%s", (id,))

# -------------------------------------------------------------------
# Countries table
# -------------------------------------------------------------------

def get_all_countries():
    # JOIN to see region names also
    sql = """
    SELECT c.*, r.region_name 
    FROM Countries c
    LEFT JOIN Regions r ON c.region_id = r.id
    ORDER BY c.country_name
    """
    return execute_query(sql, fetch=True)

def get_country_by_code(country_code):
    sql = "SELECT * FROM Countries WHERE country_code = %s"
    results = execute_query(sql, (country_code,), fetch=True)
    return results[0] if results else None

def add_country(code, name, capital, region_id, income_level):
    sql = """
    INSERT INTO Countries (country_code, country_name, capital_city, region_id, income_level)
    VALUES (%s, %s, %s, %s, %s)
    """
    return execute_query(sql, (code, name, capital, region_id, income_level))

def update_country(original_code, code, name, capital, region_id, income_level):
    sql = """
    UPDATE Countries 
    SET country_code=%s, country_name=%s, capital_city=%s, region_id=%s, income_level=%s
    WHERE country_code=%s
    """
    return execute_query(sql, (code, name, capital, region_id, income_level, original_code))

def delete_country(country_code):
    return execute_query("DELETE FROM Countries WHERE country_code=%s", (country_code,))

# -------------------------------------------------------------------
# Indicators Table
# -------------------------------------------------------------------

def get_all_indicators():

    # Dual JOIN to see its category and source
    sql = """
    SELECT i.*, c.category_name, s.source_name
    FROM Indicators i
    LEFT JOIN IndicatorCategories c ON i.category_id = c.id
    LEFT JOIN Sources s ON i.source_id = s.id
    ORDER BY i.indicator_name
    """
    return execute_query(sql, fetch=True)

def get_indicator_by_code(code):
    sql = "SELECT * FROM Indicators WHERE indicator_code = %s"
    results = execute_query(sql, (code,), fetch=True)
    return results[0] if results else None

def add_indicator(code, name, definition, unit, cat_id, source_id):
    sql = """
    INSERT INTO Indicators 
    (indicator_code, indicator_name, long_definition, unit_of_measure, category_id, source_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    return execute_query(sql, (code, name, definition, unit, cat_id, source_id))

def update_indicator(original_code, code, name, definition, unit, cat_id, source_id):
    sql = """
    UPDATE Indicators 
    SET indicator_code=%s, indicator_name=%s, long_definition=%s, 
        unit_of_measure=%s, category_id=%s, source_id=%s
    WHERE indicator_code=%s
    """
    return execute_query(sql, (code, name, definition, unit, cat_id, source_id, original_code))

def delete_indicator(code):
    return execute_query("DELETE FROM Indicators WHERE indicator_code=%s", (code,))

# -------------------------------------------------------------------
# IndicatorData Table
# -------------------------------------------------------------------

def get_all_indicator_data(limit=100):
    """List all indicator data with country & indicator names"""
    sql = """
    SELECT d.id, c.country_name, i.indicator_name, d.year, d.value, d.footnote
    FROM IndicatorData d
    JOIN Countries c ON d.country_code = c.country_code
    JOIN Indicators i ON d.indicator_code = i.indicator_code
    ORDER BY d.year DESC
    LIMIT %s
    """
    return execute_query(sql, (limit,), fetch=True)

def get_data_by_country(country_code):
    """Get all indicator data for one country"""
    sql = """
    SELECT d.*, i.indicator_name
    FROM IndicatorData d
    JOIN Indicators i ON d.indicator_code = i.indicator_code
    WHERE d.country_code = %s
    ORDER BY d.year DESC
    """
    return execute_query(sql, (country_code,), fetch=True)

def get_data_by_indicator_and_year(indicator_code, year):
    """Get all countries’ data for a specific indicator/year"""
    sql = """
    SELECT d.*, c.country_name
    FROM IndicatorData d
    JOIN Countries c ON d.country_code = c.country_code
    WHERE d.indicator_code = %s AND d.year = %s
    ORDER BY d.value DESC
    """
    return execute_query(sql, (indicator_code, year), fetch=True)

def add_indicator_data(country_code, indicator_code, year, value, footnote=""):
    sql = """
    INSERT INTO IndicatorData (country_code, indicator_code, year, value, footnote)
    VALUES (%s, %s, %s, %s, %s)
    """
    return execute_query(sql, (country_code, indicator_code, year, value, footnote))

def update_indicator_data(id, value, footnote):
    """Update numeric value or footnote for a row"""
    sql = "UPDATE IndicatorData SET value=%s, footnote=%s WHERE id=%s"
    return execute_query(sql, (value, footnote, id))

def delete_indicator_data(id):
    """Delete a record by ID"""
    sql = "DELETE FROM IndicatorData WHERE id=%s"
    return execute_query(sql, (id,))
