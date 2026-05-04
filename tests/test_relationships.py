import pandas as pd
from sqlalchemy import create_engine, text
from config import load_config


def test_db_relationships():
    params = load_config()
    # Using the safe port logic discussed earlier
    port = params.get('port', '5432')
    connection_uri = f"postgresql://{params['user']}:{params['password']}@{params['host']}:{port}/{params['database']}"

    engine = create_engine(connection_uri)

    tests = {
        "Product -> Brand & Category": """
            SELECT p.product_name, b.brand_name, c.category_name, p.price
            FROM product p
            JOIN brand b ON p.brand_id = b.brand_id
            JOIN category c ON p.category_id = c.category_id
            LIMIT 5;
        """,
        "Order -> Seller -> Order Items": """
            SELECT o.order_id, s.seller_name, oi.subtotal, o.status
            FROM "order" o
            JOIN seller s ON o.seller_id = s.seller_id
            JOIN order_item oi ON o.order_id = oi.order_id
            LIMIT 5;
        """,
        "Promotion -> Product Mapping": """
            SELECT pr.promotion_name, p.product_name, pr.discount_value
            FROM promotion_product pp
            JOIN promotion pr ON pp.promotion_id = pr.promotion_id
            JOIN product p ON pp.product_id = p.product_id
            LIMIT 5;
        """,
        "Category Hierarchy (Self-Join)": """
            SELECT child.category_name AS sub_category, parent.category_name AS main_category
            FROM category child
            JOIN category parent ON child.parent_category_id = parent.category_id
            WHERE child.level = 2
            LIMIT 5;
        """
    }

    try:
        with engine.connect() as conn:
            for test_name, query in tests.items():
                print(f"\n--- Testing Relationship: {test_name} ---")
                df = pd.read_sql_query(text(query), conn)

                if df.empty:
                    print(f"Relationship Test Failed: No data returned. Check your FK mappings.")
                else:
                    print(f"Success! Sample linked data:")
                    print(df.to_string(index=False))

    except Exception as e:
        print(f"Database Error: {e}")


if __name__ == '__main__':
    test_db_relationships()