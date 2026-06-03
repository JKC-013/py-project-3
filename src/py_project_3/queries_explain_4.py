import psycopg2
from config import load_config

def run_queries():
    params = load_config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    test_queries = [
        "SELECT TO_CHAR(order_date, 'YYYY-MM') as month, SUM(total_amount) FROM \"order\" GROUP BY month;",
        "SELECT * FROM \"order\" WHERE seller_id = 1 AND order_date >= '2025-09-01';",
        "SELECT * FROM order_item WHERE product_id = 100 LIMIT 100;",
        "SELECT * FROM \"order\" ORDER BY total_amount DESC LIMIT 1;",
        "SELECT product_id, SUM(quantity) as qty FROM order_item GROUP BY product_id ORDER BY qty DESC LIMIT 10;",
        "SELECT * FROM \"order\" WHERE seller_id = 1 AND order_date >= '2025-10-01' AND order_date < '2025-11-01';",
        "SELECT product_id, TO_CHAR(order_date, 'YYYY-MM') as m, SUM(subtotal) FROM order_item GROUP BY 1, 2;",
        "SELECT o.seller_id, SUM(oi.quantity) FROM \"order\" o JOIN order_item oi ON o.order_id = oi.order_id GROUP BY 1;"
    ]

    for i, q in enumerate(test_queries, 1):
        print(f"\n--- Query {i} Execution Plan ---")
        cur.execute(f"EXPLAIN ANALYZE {q}")
        for row in cur.fetchall():
            print(row[0])

    cur.close()
    conn.close()

if __name__ == "__main__":
    run_queries()