import psycopg2
from config import load_config


def optimize_database():
    params = load_config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    queries = [
        # Rename original tables
        'ALTER TABLE "order" RENAME TO order_old;',
        'ALTER TABLE order_item RENAME TO order_item_old;',

        # Create partitioned Order table (Copy structure, but NOT old constraints)
        '''CREATE TABLE "order" (LIKE order_old INCLUDING DEFAULTS) 
           PARTITION BY RANGE (order_date);''',

        # Add the required composite Primary Key
        'ALTER TABLE "order" ADD PRIMARY KEY (order_id, order_date);',

        # Create Order Partitions
        '''CREATE TABLE order_2025_08 PARTITION OF "order" 
           FOR VALUES FROM ('2025-08-01') TO ('2025-09-01');''',
        '''CREATE TABLE order_2025_09 PARTITION OF "order" 
           FOR VALUES FROM ('2025-09-01') TO ('2025-10-01');''',
        '''CREATE TABLE order_2025_10 PARTITION OF "order" 
           FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');''',

        # Create partitioned Order Item table (Copy structure, but NOT old constraints)
        '''CREATE TABLE order_item (LIKE order_item_old INCLUDING DEFAULTS) 
           PARTITION BY RANGE (order_date);''',

        # Add the required composite Primary Key
        'ALTER TABLE order_item ADD PRIMARY KEY (order_item_id, order_date);',

        # Create Order Item Partitions
        '''CREATE TABLE order_item_2025_08 PARTITION OF order_item 
           FOR VALUES FROM ('2025-08-01') TO ('2025-09-01');''',
        '''CREATE TABLE order_item_2025_09 PARTITION OF order_item 
           FOR VALUES FROM ('2025-09-01') TO ('2025-10-01');''',
        '''CREATE TABLE order_item_2025_10 PARTITION OF order_item 
           FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');''',

        # Move data from old tables to new partitioned tables
        'INSERT INTO "order" SELECT * FROM order_old;',
        'INSERT INTO order_item SELECT * FROM order_item_old;',

        # Create Required Index for performance
        'CREATE INDEX idx_order_item_product_id ON order_item(product_id);',

        # Cleanup old tables (CASCADE handles dropping any old lingering views/constraints)
        'DROP TABLE order_old CASCADE;',
        'DROP TABLE order_item_old CASCADE;'
    ]

    for q in queries:
        cur.execute(q)

    conn.commit()
    cur.close()
    conn.close()
    print("Database partitions and indexes created successfully.")


if __name__ == "__main__":
    optimize_database()