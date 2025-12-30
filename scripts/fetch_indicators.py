import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import re
from database.db_connect import get_connection

API = "https://api.worldbank.org/v2/indicator?format=json&per_page=20000"


def normalize_topic_id(value: str) -> str:
    if not value:
        return None
    value = value.upper()
    value = re.sub(r'[^A-Z0-9]+', '_', value)
    value = value.strip('_')
    return value


def fetch_indicators():
    print("Fetching indicator metadata...")
    resp = requests.get(API)
    resp.raise_for_status()
    data = resp.json()
    indicators = data[1]
    print(f"Fetched {len(indicators)} indicators.")
    return indicators


def import_categories(topic_set):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT IGNORE INTO IndicatorCategories (id, category_name, topic, description)
    VALUES (%s, %s, %s, %s)
    """

    for tid, name in topic_set:
        cursor.execute(sql, (
            tid,
            name,
            name,
            None
        ))

    conn.commit()
    cursor.close()
    conn.close()


def import_sources(source_map):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT IGNORE INTO Sources (id, source_name, source_organization, source_url, description)
    VALUES (%s, %s, %s, %s, %s)
    """

    for sid, s in source_map.items():
        cursor.execute(sql, (
            sid,
            s["name"],
            s["organization"],
            s["url"],
            None
        ))

    conn.commit()
    cursor.close()
    conn.close()


def import_indicators(indicators):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT IGNORE INTO Indicators
    (indicator_code, indicator_name, long_definition, unit_of_measure, category_id, source_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    inserted = 0
    seen = set()

    for ind in indicators:
        code = ind.get("id")

        if not code:
            continue

        # SKIP duplicates
        if code in seen:
            continue
        seen.add(code)

        name = ind.get("name")
        long_def = ind.get("sourceNote")
        unit = ind.get("unit")

        # topic
        topics = ind.get("topics", [])
        if topics:
            t = topics[0]
            tid = t.get("id") or normalize_topic_id(t.get("value"))
        else:
            tid = None

        # source
        src = ind.get("source", {})
        sid = src.get("id")

        cursor.execute(sql, (
            code,
            name,
            long_def,
            unit,
            tid,
            sid
        ))
        inserted += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted {inserted} indicators.")


def main():
    indicators = fetch_indicators()

    # Collect topics
    topic_set = set()
    for ind in indicators:
        for t in ind.get("topics", []):
            tid = t.get("id") or normalize_topic_id(t.get("value"))
            tval = t.get("value")
            topic_set.add((tid, tval))

    print(f"Unique topics: {len(topic_set)}")
    import_categories(topic_set)

    # Collect sources
    source_map = {}
    for ind in indicators:
        src = ind.get("source", {})
        sid = src.get("id")
        if sid: 
            source_map[sid] = {
                "name": src.get("value"),
                "organization": src.get("organization"),
                "url": src.get("url")
            }
    print(f"Unique sources: {len(source_map)}")
    import_sources(source_map)

    import_indicators(indicators)


if __name__ == "__main__":
    main()
