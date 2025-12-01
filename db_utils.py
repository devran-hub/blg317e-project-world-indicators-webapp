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
def get_all_regions():
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


# ---------------------------------------------
# SOURCES
# ---------------------------------------------
def get_all_sources():
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

def delete_source(id):
    return execute("DELETE FROM Sources WHERE id=%s", (id,))


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
def get_all_countries():
    return execute(
        """
        SELECT C.*, R.region_name
        FROM Countries C
        LEFT JOIN Regions R ON C.region_id = R.id
        ORDER BY C.country_name
        """,
        fetch=True
    )

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
def get_all_indicators():
    return execute(
        """
        SELECT I.*, C.category_name, S.source_name
        FROM Indicators I
        LEFT JOIN IndicatorCategories C ON I.category_id = C.id
        LEFT JOIN Sources S ON I.source_id = S.id
        ORDER BY I.indicator_name
        """,
        fetch=True
    )

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

def add_indicator(code, name, definition, unit, cat_id, source_id):
    return execute(
        """
        INSERT INTO Indicators
        (indicator_code, indicator_name, long_definition, unit_of_measure, category_id, source_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (code, name, definition, unit, cat_id, source_id)
    )

def delete_indicator(code):
    return execute("DELETE FROM Indicators WHERE indicator_code=%s", (code,))


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
