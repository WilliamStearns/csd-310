#William Stearns
#CS 310 Milestone 3
#5-9-25
# This script connects to a MySQL database and runs several queries to generate reports.
from dotenv import load_dotenv
from tabulate import tabulate
import os
import mysql.connector
from contextlib import contextmanager

# Load credentials
load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("HOST"),
    "user":     os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "database": os.getenv("DATABASE"),
}

@contextmanager
def mysql_connection(cfg: dict):
    conn = None
    try:
        conn = mysql.connector.connect(**cfg)
        yield conn
    finally:
        if conn and conn.is_connected():
            conn.close()

def run_and_show(cur, title: str, sql: str):
    cur.execute(sql)
    rows = cur.fetchall()
    headers = [d[0] for d in cur.description]

    print("\n" + "=" * 80)
    print(f"{title.center(80)}")
    print("=" * 80)
    print(
        tabulate(
            rows,
            headers=headers,
            tablefmt="fancy_grid",
            numalign="right",
            stralign="left"
        )
    )
    print(f"\n{len(rows)} row(s) returned\n")

def main():
    queries = {
        "Supplier Delivery Timeliness by Month": """
            SELECT
                s.supplier_name      AS Supplier,
                MONTH(so.date_expected) AS Month,
                COUNT(*)                AS Total_Orders,
                SUM(DATEDIFF(so.date_received, so.date_expected)) AS Total_Days_Late
            FROM supply_orders so
            JOIN suppliers s ON so.supplier_id = s.supplier_id
            WHERE so.date_received IS NOT NULL
            GROUP BY Supplier, Month
            ORDER BY Supplier, Month;
        """,
        "Wine Sales and Distributors": """
            SELECT
                w.wine_name        AS Wine,
                d.distributor_name AS Distributor,
                SUM(wod.quantity)  AS Cases_Sold
            FROM wine_order_details   wod
            JOIN wines               w  ON wod.wine_id      = w.wine_id
            JOIN distributor_orders  do ON wod.wine_order_id = do.wine_order_id
            JOIN distributors        d  ON do.distributor_id = d.distributor_id
            GROUP BY Wine, Distributor
            ORDER BY Wine, Cases_Sold DESC;
        """,
        "Employee Hours by Quarter": """
            SELECT
                e.first_name  AS First_Name,
                e.last_name   AS Last_Name,
                h.quarter     AS Quarter,
                SUM(h.hours)  AS Hours
            FROM hours h
            JOIN employees e ON h.employee_id = e.employee_id
            GROUP BY e.employee_id, Quarter
            ORDER BY Last_Name, Quarter;
        """
    }

    with mysql_connection(DB_CONFIG) as conn, conn.cursor() as cur:
        for title, sql in queries.items():
            run_and_show(cur, title, sql)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        raise