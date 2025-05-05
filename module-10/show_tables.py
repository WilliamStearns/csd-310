#William Stearns
#5-4-2025
#Display every table in the winery schema.



import mysql.connector
from pprint import pprint

# Update connection settings if yours differ
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="winery"
)

cursor = conn.cursor()
cursor.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'winery'
    ORDER BY table_name;
""")
tables = [row[0] for row in cursor.fetchall()]

for t in tables:
    print("\n" + "="*15, t.upper(), "="*15)
    cursor.execute(f"SELECT * FROM {t};")
    rows = cursor.fetchall()
    col_names = [d[0] for d in cursor.description]
    print(col_names)
    for r in rows:
        pprint(r)

cursor.close()
conn.close()