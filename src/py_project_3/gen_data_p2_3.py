import random
from datetime import timedelta
from faker import Faker
import psycopg2
from config import load_config

fake = Faker('vi_VN')


def get_ids(cur, table_name, id_column):
    cur.execute(f"SELECT {id_column} FROM {table_name}")
    return [r[0] for r in cur.fetchall()]


def run_p2():
    conn = None
    try:
        params = load_config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # Get existing IDs from Part 1
        seller_ids = get_ids(cur, 'seller', 'seller_id')
        product_ids = get_ids(cur, 'product', 'product_id')

        # 5. Order (100 rows)
        orders = [(fake.date_time_between(start_date='-1y'), random.choice(seller_ids),
                   random.choice(['PLACED', 'PAID', 'SHIPPED', 'DELIVERED']), 0) for _ in range(100)]
        cur.executemany('INSERT INTO "order" (order_date, seller_id, status, total_amount) VALUES (%s, %s, %s, %s)',
                        orders)
        conn.commit()
        print("Inserted 100 Orders.")

        # 6. Order Item (Linked to Orders and Products)
        order_ids = get_ids(cur, '"order"', 'order_id')
        order_items = []
        for o_id in order_ids:
            for _ in range(random.randint(1, 4)):  # 1-4 items per order
                u_price = random.uniform(100000, 1000000)
                qty = random.randint(1, 3)
                order_items.append((o_id, random.choice(product_ids), qty, u_price, qty * u_price))
        cur.executemany(
            "INSERT INTO order_item (order_id, product_id, quantity, unit_price, subtotal) VALUES (%s,%s,%s,%s,%s)",
            order_items)
        print(f"Inserted {len(order_items)} Order Items.")

        # 7. Promotion (10 rows)
        promotions = []
        for _ in range(10):
            start = fake.date_between(start_date='-1y', end_date='today')
            promotions.append((f"{fake.word().upper()} SALE", random.choice(['product', 'flash_sale']),
                               random.choice(['percentage', 'fixed_amount']), random.choice([10.0, 50000.0]),
                               start, start + timedelta(days=random.randint(7, 30))))
        cur.executemany(
            "INSERT INTO promotion (promotion_name, promotion_type, discount_type, discount_value, start_date, end_date) VALUES (%s,%s,%s,%s,%s,%s)",
            promotions)
        conn.commit()
        print("Inserted 10 Promotions.")

        # 8. Promotion Product (100 mappings)
        promo_ids = get_ids(cur, 'promotion', 'promotion_id')
        promo_prods = [(random.choice(promo_ids), random.choice(product_ids)) for _ in range(100)]
        cur.executemany("INSERT INTO promotion_product (promotion_id, product_id) VALUES (%s, %s)", promo_prods)

        conn.commit()
        print("Inserted 100 Promotion-Product mappings. Part 2 Complete.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn: conn.close()


if __name__ == '__main__':
    run_p2()