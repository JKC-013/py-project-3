import random
from faker import Faker
import psycopg2
from config import load_config

fake = Faker('vi_VN')

def get_ids(cur, table_name, id_column):
    cur.execute(f"SELECT {id_column} FROM {table_name}")
    return [r[0] for r in cur.fetchall()]

def run_p1():
    conn = None
    try:
        params = load_config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # 1. Brand (20 rows)
        brands = [(fake.company(), fake.country(), fake.date_time_between(start_date='-5y')) for _ in range(20)]
        cur.executemany("INSERT INTO brand (brand_name, country, created_at) VALUES (%s, %s, %s)", brands)
        print("Inserted 20 Brands.")

        # 2. Category (10 rows)
        main_cats = [("Electronics", None, 1), ("Fashion", None, 1), ("Home & Living", None, 1)]
        cur.executemany("INSERT INTO category (category_name, parent_category_id, level) VALUES (%s, %s, %s)", main_cats)
        conn.commit()

        cur.execute("SELECT category_id FROM category WHERE level = 1")
        main_cat_ids = [r[0] for r in cur.fetchall()]
        sub_cats = [(fake.word().capitalize(), random.choice(main_cat_ids), 2) for _ in range(7)]
        cur.executemany("INSERT INTO category (category_name, parent_category_id, level) VALUES (%s, %s, %s)", sub_cats)
        print("Inserted 10 Categories.")

        # 3. Seller (25 rows)
        sellers = [(fake.company(), fake.date_between(start_date='-3y'), random.choice(['Official', 'Marketplace']),
                    round(random.uniform(3.0, 5.0), 1), 'Vietnam') for _ in range(25)]
        cur.executemany("INSERT INTO seller (seller_name, join_date, seller_type, rating, country) VALUES (%s, %s, %s, %s, %s)", sellers)
        print("Inserted 25 Sellers.")
        conn.commit()

        # 4. Product (2000 rows)
        brand_ids = get_ids(cur, 'brand', 'brand_id')
        cat_ids = get_ids(cur, 'category', 'category_id')
        seller_ids = get_ids(cur, 'seller', 'seller_id')

        products = []
        for _ in range(2000):
            price = random.uniform(100000, 50000000)
            products.append((fake.catch_phrase(), random.choice(cat_ids), random.choice(brand_ids),
                             random.choice(seller_ids), price, price * random.uniform(0.7, 0.95),
                             random.randint(0, 500), round(random.uniform(3.0, 5.0), 1),
                             fake.date_time_between(start_date='-3y'), random.choice([True, False])))

        cur.executemany("""INSERT INTO product (product_name, category_id, brand_id, seller_id, price, discount_price, 
                           stock_qty, rating, created_at, is_active) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", products)

        conn.commit()
        print("Inserted 2000 Products. Part 1 Complete.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn: conn.close()

if __name__ == '__main__':
    run_p1()