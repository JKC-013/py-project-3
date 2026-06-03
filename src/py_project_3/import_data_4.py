import os
import psycopg2
from config import load_config

def import_csvs():
    params = load_config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    orders_path = os.path.abspath('orders.csv')
    items_path = os.path.abspath('items.csv')

    print("Clearing old data...")
    cur.execute('TRUNCATE TABLE "order" CASCADE;')
    conn.commit()

    # Import orders
    print("Importing orders (this may take a minute)...")
    with open(orders_path, 'r') as f:
        cur.copy_expert("""
            COPY "order"(order_id, order_date, seller_id, status, total_amount, created_at) 
            FROM STDIN WITH CSV
        """, f)

    # Import items
    print("Importing order items (this may take a few minutes)...")
    with open(items_path, 'r') as f:
        cur.copy_expert("""
            COPY order_item(order_id, product_id, order_date, quantity, unit_price, subtotal, created_at) 
            FROM STDIN WITH CSV
        """, f)

    conn.commit()
    cur.close()
    conn.close()

    # Clean up massive text files
    os.remove(orders_path)
    os.remove(items_path)
    print("Data imported and temporary CSV files removed.")

if __name__ == "__main__":
    import_csvs()