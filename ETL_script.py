import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres_db",
    user="root",
    password="root"
)

cursor = conn.cursor()

create_table_queries = [
    """
    CREATE TABLE IF NOT EXISTS table1 (
        id SERIAL PRIMARY KEY,
        isim VARCHAR(255),
        soyisim VARCHAR(255),
        dateofbirth DATE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS table2 (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255),
        yas INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXIST table3 (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    username VARCHAR(255)
    )
    
    """
]
for query in create_table_queries:
    cursor.execute(query)

    