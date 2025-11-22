import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import time
from database.db_connect import get_connection

# Seçtiğimiz 10 adet core indicator
INDICATORS = [
    "NY.GDP.MKTP.CD",    # GDP (current US$)
    "NY.GDP.PCAP.CD",    # GDP per capita (current US$)
    "SP.POP.TOTL",       # Population, total
    "SP.DYN.LE00.IN",    # Life expectancy, total
    "EN.ATM.CO2E.KT",    # CO2 emissions (kt)
    "FP.CPI.TOTL.ZG",    # Inflation (annual %)
    "NE.TRD.GNFS.ZS",    # Trade (% of GDP)
    "SL.UEM.TOTL.ZS",    # Unemployment (% labor force)
    "SE.PRM.ENRR",       # School enrollment (% gross)
    "EG.USE.PCAP.KG.OE"  # Energy use
]

START_YEAR = 2000
END_YEAR = 2023


def fetch_indicator_all(indicator_code):
    """Tek API çağrısı ile tüm ülkeler için tüm yılları getir."""
    url = (
        f"https://api.worldbank.org/v2/country/all/indicator/"
        f"{indicator_code}?format=json&per_page=20000"
    )

    for attempt in range(5):
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            if len(data) < 2 or data[1] is None:
                return []
            return data[1]

        if resp.status_code in (500, 502, 503, 504):
            print(f"[{indicator_code}] Server {resp.status_code}, retry {attempt+1}/5")
            time.sleep(1)
            continue

        resp.raise_for_status()

    print(f"[{indicator_code}] SKIPPED: API unreachable.")
    return []


def insert_batch(records):
    """IndicatorData tablosuna batch insert."""
    if not records:
        return 0

    conn = get_connection()
    cursor_insert = conn.cursor()
    cursor_check = conn.cursor()

    sql_insert = """
        INSERT INTO IndicatorData (country_code, indicator_code, year, value)
        VALUES (%s, %s, %s, %s)
    """

    inserted = 0

    for (country_code, indicator_code, year, value) in records:

        # FK valid country kontrolü
        cursor_check.execute(
            "SELECT 1 FROM Countries WHERE country_code = %s",
            (country_code,)
        )
        if cursor_check.fetchone() is None:
            continue  # aggregate, region, group → SKIP

        cursor_insert.execute(sql_insert, (country_code, indicator_code, year, value))
        inserted += 1

    conn.commit()
    cursor_insert.close()
    cursor_check.close()
    conn.close()

    return inserted


def main():
    total_inserted = 0

    for indicator in INDICATORS:
        print(f"\n=== Processing indicator: {indicator} ===")

        observations = fetch_indicator_all(indicator)
        print(f"Raw observations: {len(observations)}")

        batch = []

        for obs in observations:

            # 🔥 DOĞRU ülke kodu (garanti çalışan)
            country_code = (
                obs.get("countryiso3code") or
                obs.get("country", {}).get("id")
            )

            year_str = obs.get("date")
            value = obs.get("value")

            # Temel filtreler
            try:
                year = int(year_str)
            except:
                continue

            if year < START_YEAR or year > END_YEAR:
                continue

            if value is None:
                continue

            batch.append((country_code, indicator, year, value))

            if len(batch) >= 5000:
                inserted = insert_batch(batch)
                total_inserted += inserted
                print(f"Inserted so far: {total_inserted}")
                batch = []

        # kalanlar
        if batch:
            inserted = insert_batch(batch)
            total_inserted += inserted
            print(f"Inserted so far: {total_inserted}")

    print(f"\nDONE. Total rows inserted: {total_inserted}")


if __name__ == "__main__":
    main()
