import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from database.db_connect import get_connection

COUNTRY_API = "https://api.worldbank.org/v2/country?format=json&per_page=400"

# 7 REAL WB REGIONS (same as Regions table)
VALID_REGIONS = {
    "EAS",
    "ECS",
    "LCN",
    "MEA",
    "NAC",
    "SAS",
    "SSF",
}


def fetch_countries():
    print("Fetching countries from World Bank API...")
    resp = requests.get(COUNTRY_API)
    resp.raise_for_status()
    data = resp.json()
    return data[1]


def build_region_map():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, region_code FROM Regions")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return {code: rid for rid, code in rows}


def import_countries():
    countries = fetch_countries()
    region_map = build_region_map()

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO Countries (country_code, country_name, capital_city, region_id, income_level)
    VALUES (%s, %s, %s, %s, %s)
    """

    inserted = 0
    skipped = 0

    for c in countries:

        country_code = c["id"]
        country_name = c["name"]
        capital_city = c["capitalCity"] or None

        region_code = c["region"]["id"]       # like "EAS", "MEA", etc.
        income_level = c["incomeLevel"]["value"] or None

        # ❌ Skip aggregates (World, High income, etc.)
        if region_code not in VALID_REGIONS:
            skipped += 1
            continue

        # ❌ Capital city boş olan entries (aggregates, regions)
        if not capital_city or capital_city.strip() == "":
            skipped += 1
            continue

        region_id = region_map.get(region_code)

        if region_id is None:
            skipped += 1
            continue

        cursor.execute(sql, (
            country_code,
            country_name,
            capital_city,
            region_id,
            income_level
        ))
        inserted += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Inserted {inserted} REAL countries.")
    print(f"Skipped {skipped} aggregate / invalid entries.")


if __name__ == "__main__":
    import_countries()
