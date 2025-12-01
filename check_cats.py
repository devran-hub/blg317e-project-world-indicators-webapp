from db_utils import get_all_categories
try:
    cats = get_all_categories()
    print("Categories found:")
    for c in cats:
        print(f"- {c['category_name']}")
except Exception as e:
    print(f"Error: {e}")
