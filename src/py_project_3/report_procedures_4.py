import psycopg2
from config import load_config

def setup_and_run_reports():
    params = load_config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    funcs = [
        "DROP FUNCTION IF EXISTS get_monthly_revenue CASCADE;",
        "DROP FUNCTION IF EXISTS get_daily_revenue CASCADE;",
        "DROP FUNCTION IF EXISTS get_seller_performance CASCADE;",
        "DROP FUNCTION IF EXISTS get_top_products_per_brand CASCADE;",
        "DROP FUNCTION IF EXISTS get_order_status_summary CASCADE;",

        # 1. Monthly Revenue
        """CREATE OR REPLACE FUNCTION get_monthly_revenue(start_d DATE, end_d DATE)
        RETURNS TABLE(month TEXT, total_orders BIGINT, qty BIGINT, rev NUMERIC) AS $$
        BEGIN RETURN QUERY SELECT TO_CHAR(o.order_date, 'YYYY-MM'), COUNT(DISTINCT o.order_id), SUM(oi.quantity), SUM(oi.subtotal)
        FROM "order" o JOIN order_item oi ON o.order_id = oi.order_id WHERE o.order_date BETWEEN start_d AND end_d GROUP BY 1; END; $$ LANGUAGE plpgsql;""",

        # 2. Daily Revenue (With optional product array filter)
        """CREATE OR REPLACE FUNCTION get_daily_revenue(start_d DATE, end_d DATE, p_list INT[] DEFAULT NULL)
        RETURNS TABLE(date DATE, total_orders BIGINT, qty BIGINT, rev NUMERIC) AS $$
        BEGIN RETURN QUERY SELECT DATE(o.order_date), COUNT(DISTINCT o.order_id), SUM(oi.quantity), SUM(oi.subtotal)
        FROM "order" o JOIN order_item oi ON o.order_id = oi.order_id WHERE o.order_date BETWEEN start_d AND end_d
        AND (p_list IS NULL OR oi.product_id = ANY(p_list)) GROUP BY 1 ORDER BY 1; END; $$ LANGUAGE plpgsql;""",

        # 3. Seller Performance
        """CREATE OR REPLACE FUNCTION get_seller_performance(start_d DATE, end_d DATE)
        RETURNS TABLE(seller_id INT, name VARCHAR, total_orders BIGINT, qty BIGINT, rev NUMERIC) AS $$
        BEGIN RETURN QUERY SELECT s.seller_id, s.seller_name, COUNT(DISTINCT o.order_id), SUM(oi.quantity), SUM(oi.subtotal)
        FROM seller s JOIN "order" o ON s.seller_id = o.seller_id JOIN order_item oi ON o.order_id = oi.order_id
        WHERE o.order_date BETWEEN start_d AND end_d GROUP BY 1, 2; END; $$ LANGUAGE plpgsql;""",

        # 4. Top Products per Brand (With optional seller array filter)
        """CREATE OR REPLACE FUNCTION get_top_products_per_brand(start_d DATE, end_d DATE, s_list INT[] DEFAULT NULL)
        RETURNS TABLE(b_id INT, b_name VARCHAR, p_id INT, p_name VARCHAR, qty BIGINT, rev NUMERIC) AS $$
        BEGIN RETURN QUERY SELECT b.brand_id, b.brand_name, p.product_id, p.product_name, SUM(oi.quantity), SUM(oi.subtotal)
        FROM brand b JOIN product p ON b.brand_id = p.brand_id JOIN order_item oi ON p.product_id = oi.product_id JOIN "order" o ON oi.order_id = o.order_id
        WHERE o.order_date BETWEEN start_d AND end_d AND (s_list IS NULL OR o.seller_id = ANY(s_list))
        GROUP BY 1, 2, 3, 4 ORDER BY b.brand_id, SUM(oi.quantity) DESC; END; $$ LANGUAGE plpgsql;""",

        # 5. Order Status Summary
        """CREATE OR REPLACE FUNCTION get_order_status_summary(start_d DATE, end_d DATE)
        RETURNS TABLE(status VARCHAR, total_orders BIGINT, rev NUMERIC) AS $$
        BEGIN RETURN QUERY SELECT o.status, COUNT(o.order_id), COALESCE(SUM(o.total_amount), 0)
        FROM "order" o WHERE o.order_date BETWEEN start_d AND end_d GROUP BY o.status; END; $$ LANGUAGE plpgsql;"""
    ]

    # Create functions
    for f in funcs: cur.execute(f)
    conn.commit()
    print("All 5 reporting functions created successfully.\n")

    # Execute and display reports (using sample dates and array filters)
    tests = [
        ("Monthly Revenue", "SELECT * FROM get_monthly_revenue('2025-08-01', '2025-10-31');"),
        ("Daily Revenue (Filtered by Product IDs 10, 50)", "SELECT * FROM get_daily_revenue('2025-08-01', '2025-08-03', ARRAY[10, 50]);"),
        ("Top 5 Sellers", "SELECT * FROM get_seller_performance('2025-08-01', '2025-10-31') ORDER BY rev DESC LIMIT 5;"),
        ("Top Products (Filtered by Seller IDs 1, 2)", "SELECT * FROM get_top_products_per_brand('2025-08-01', '2025-10-31', ARRAY[1, 2]) LIMIT 5;"),
        ("Status Summary", "SELECT * FROM get_order_status_summary('2025-08-01', '2025-10-31');")
    ]

    for title, query in tests:
        print(f"--- {title} ---")
        cur.execute(query)
        cols = [desc[0] for desc in cur.description]
        print(f"{' | '.join(cols)}")
        for row in cur.fetchall():
            print(row)
        print("")

    cur.close()
    conn.close()

if __name__ == "__main__":
    setup_and_run_reports()