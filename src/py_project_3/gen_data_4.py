import csv
import random
from datetime import datetime
import psycopg2
from config import load_config


def generate_csv_data():
    params = load_config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute("SELECT seller_id, product_id, price FROM product")

    # Map products to sellers: {seller_id: [(product_id, price), ...]}
    catalog = {}
    for sid, pid, price in cur.fetchall():
        catalog.setdefault(sid, []).append((pid, price))

    valid_sellers = [s for s, p in catalog.items() if len(p) >= 4]
    start_ts = int(datetime(2025, 8, 1).timestamp())
    end_ts = int(datetime(2025, 10, 31).timestamp())

    statuses = ['PLACED', 'PAID', 'DELIVERED', 'SHIPPED', 'CANCELLED', 'RETURNED']
    weights = [0.05, 0.04, 0.70, 0.11, 0.07, 0.03]
    num_orders = random.randint(2500000, 3000000)

    print(f"Generating {num_orders} orders...")
    with open('orders.csv', 'w', newline='') as fo, open('items.csv', 'w', newline='') as fi:
        order_writer, item_writer = csv.writer(fo), csv.writer(fi)

        order_id = 1
        for _ in range(num_orders):
            seller_id = random.choice(valid_sellers)
            dt = datetime.fromtimestamp(random.randint(start_ts, end_ts))
            status = random.choices(statuses, weights=weights)[0]

            selected_prods = random.sample(catalog[seller_id], random.randint(3, 4))
            total_amount = 0
            items_to_write = []

            for pid, price in selected_prods:
                qty = random.randint(1, 5)
                sub = qty * price
                total_amount += sub
                # No order_item_id here; BIGSERIAL will auto-generate it during COPY
                items_to_write.append([order_id, pid, dt, qty, price, sub, dt])

            order_writer.writerow([order_id, dt, seller_id, status, total_amount, dt])
            item_writer.writerows(items_to_write)
            order_id += 1


if __name__ == "__main__":
    generate_csv_data()
    print("CSV files generated successfully.")