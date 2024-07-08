import psycopg2
import time

RETRY_ATTEMPTS = 20
RETRY_DELAY = 5

for attempt in range(RETRY_ATTEMPTS):
    try:
        db = psycopg2.connect(
            database = "test_db",
            user = "root",
            password = "root",
            host = "db",
            port = "5432"
        )
        print("BAGLANDI")
        break
    except psycopg2.OperationalError as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        time.sleep(RETRY_DELAY)
else:
    print("All attempts to connect to the database failed.")
    exit(1)

create_table_queries = [
    """
    CREATE TABLE IF NOT EXISTS table1 (
        id SERIAL PRIMARY KEY,
        isim VARCHAR(255),
        soyisim VARCHAR(255),
        dateofbirth DATE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS table2 (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255),
        yas INTEGER
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS table3 (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        username VARCHAR(255)
    );
    """
]

with db.cursor() as cursor:
    for query in create_table_queries:
        try:
            cursor.execute(query)
            print(f"Executed query: {query}")
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")

db.commit()  # Ensure changes are committed
db.close()  # Close the connection
