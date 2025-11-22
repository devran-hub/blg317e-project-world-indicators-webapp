import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from database.db_connect import get_connection

API = "https://api.worldbank.org/V2/region/?format=json&per_page=500"

VALID_REGIONS = {
    "EAS",  # East Asia & Pacific
    "ECS",  # Europe & Central Asia
    "LCN",  # Latin America & Caribbean
    "MEA",  # Middle East & North Africa
    "NAC",  # North America
    "SAS",  # South Asia
    "SSF",  # Sub-Saharan Africa
}

def import_regions():
    print("Fetching REAL regions metadata...")
    resp = requests.get(API)
    resp.raise_for_status()
    data = resp.json()

    regions = data[1]
    print(f"Fetched {len(regions)} raw regions from API.")

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO Regions (region_code, region_name)
    VALUES (%s, %s)
    """

    inserted = 0
    skipped = 0

    for r in regions:
        region_code = r.get("code")

        # ❗ sadece 7 gerçek region’u al
        if region_code not in VALID_REGIONS:
            skipped += 1
            continue

        region_name = r.get("name")
        

        cursor.execute(sql, (
            region_code,
            region_name,
            
        ))

        inserted += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Inserted {inserted} REAL regions.")
    print(f"Skipped {skipped} non-geographic/aggregate regions.")


if __name__ == "__main__":
    import_regions()
