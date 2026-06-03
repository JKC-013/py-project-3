import psycopg2
from config import load_config


def create_tables():
    params = load_config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute("""
        DROP TABLE IF EXISTS order_item CASCADE;
        DROP TABLE IF EXISTS "order" CASCADE;

        -- Create order table
        CREATE TABLE "order" (
            order_id SERIAL PRIMARY KEY,
            order_date TIMESTAMP,
            seller_id INT REFERENCES seller(seller_id),
            status VARCHAR(20),
            total_amount DECIMAL(12,2),
            created_at TIMESTAMP
        );

        -- Create order_item table
        CREATE TABLE order_item (
            order_item_id BIGSERIAL PRIMARY KEY,
            order_id INT REFERENCES "order"(order_id),
            product_id INT REFERENCES product(product_id),
            order_date TIMESTAMP, -- MAKE SURE THIS LINE EXISTS!
            quantity INT,
            unit_price NUMERIC(10,2),
            subtotal NUMERIC(12,2),
            created_at TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Tables 'order' and 'order_item' created successfully.")


if __name__ == "__main__":
    create_tables()