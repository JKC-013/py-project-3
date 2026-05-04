import psycopg2
import pandas as pd
from config import load_config


def view_data_with_counts():
    # Note: "order" is a reserved keyword, so we keep the double quotes
    tables = [
        'brand',
        'category',
        'seller',
        'product',
        'promotion',
        'promotion_product',
        '"order"',
        'order_item'
    ]

    conn = None
    try:
        params = load_config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        for table in tables:
            print(f"\n{'=' * 50}")

            # 1. Get the Total Count
            cur.execute(f"SELECT COUNT(*) FROM {table};")
            count = cur.fetchone()[0]

            print(f" TABLE: {table.replace('\"', '')}")
            print(f" TOTAL ROWS: {count}")
            print(f"{'-' * 50}")

            # 2. Get the Top 5 Rows
            query = f"SELECT * FROM {table} LIMIT 5;"
            df = pd.read_sql_query(query, conn)

            if df.empty:
                print(" (Table is currently empty)")
            else:
                print(df.to_string(index=False))

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    view_data_with_counts()