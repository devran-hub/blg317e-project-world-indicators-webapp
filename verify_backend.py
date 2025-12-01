from db_utils import get_indicators_by_category_name

categories = ['Health', 'Education', 'Economy']

for cat in categories:
    print(f"--- Testing category: {cat} ---")
    try:
        indicators = get_indicators_by_category_name(cat)
        print(f"Found {len(indicators)} indicators.")
        for i in indicators[:3]:
            print(f"  - {i['indicator_name']} (Category: {i['category_name']})")
    except Exception as e:
        print(f"Error: {e}")
    print("\n")
