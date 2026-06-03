import psycopg2
from config import load_config


def create_tables():
    """ Create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE brand
        (
            brand_id   SERIAL PRIMARY KEY,
            brand_name VARCHAR(100) NOT NULL,
            country    VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE category
        (
            category_id        SERIAL PRIMARY KEY,
            category_name      VARCHAR(100) NOT NULL,
            parent_category_id INT REFERENCES category (category_id),
            level              SMALLINT     NOT NULL,
            created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE seller
        (
            seller_id   SERIAL PRIMARY KEY,
            seller_name VARCHAR(150) NOT NULL,
            join_date   DATE         NOT NULL,
            seller_type VARCHAR(50),
            rating      DECIMAL(2, 1),
            country     VARCHAR(50) DEFAULT 'Vietnam'
        )
        """,
        """
        CREATE TABLE promotion
        (
            promotion_id   SERIAL PRIMARY KEY,
            promotion_name VARCHAR(100) NOT NULL,
            promotion_type VARCHAR(50),
            discount_type  VARCHAR(20),
            discount_value NUMERIC(10, 2),
            start_date     DATE,
            end_date       DATE
        )
        """,
        """
        CREATE TABLE product
        (
            product_id     SERIAL PRIMARY KEY,
            product_name   VARCHAR(200)   NOT NULL,
            category_id    INT REFERENCES category (category_id),
            brand_id       INT REFERENCES brand (brand_id),
            seller_id      INT REFERENCES seller (seller_id),
            price          DECIMAL(12, 2) NOT NULL,
            discount_price DECIMAL(12, 2),
            stock_qty      INT       DEFAULT 0,
            rating         FLOAT,
            created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active      BOOLEAN   DEFAULT TRUE
        )
        """,
        """
        CREATE TABLE "order"
        (
            order_id     SERIAL PRIMARY KEY,
            order_date   TIMESTAMP NOT NULL,
            seller_id    INT REFERENCES seller (seller_id),
            status       VARCHAR(20),
            total_amount DECIMAL(12, 2),
            created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE order_item
        (
            order_item_id SERIAL PRIMARY KEY,
            order_id      INT REFERENCES "order" (order_id),
            product_id    INT REFERENCES product (product_id),
            quantity      INT            NOT NULL,
            unit_price    DECIMAL(12, 2) NOT NULL,
            subtotal      DECIMAL(12, 2) NOT NULL
        )
        """,
        """
        CREATE TABLE promotion_product
        (
            promo_product_id SERIAL PRIMARY KEY,
            promotion_id     INT REFERENCES promotion (promotion_id),
            product_id       INT REFERENCES product (product_id),
            created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn = None
    try:
        params = load_config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # Create tables one by one
        for command in commands:
            cur.execute(command)

        cur.close()
        conn.commit()
        print("All tables created successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()