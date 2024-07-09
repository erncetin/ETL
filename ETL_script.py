import psycopg2
from faker import Faker
from time import time
from datetime import datetime

fake = Faker()

try:
        db = psycopg2.connect(
            database = "test_db",
            user = "root",
            password = "root",
            host = "db",
            port = "5432"
        )
        print("BAGLANDI")
except psycopg2.OperationalError as e:
        print(f"failed to connect to database: {e}")


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
        age VARCHAR(255),
        dateofbirth VARCHAR(255)

    );
    """
]

with db.cursor() as cursor:
    for query in create_table_queries:
        try:
            cursor.execute(query)
            print(f"Executed query: {query}")
            db.commit()
        except psycopg2.Error as e:
            db.rollback()
            print(f"Error executing query: {e}")

name_list = [fake.first_name() for _ in range(100)]
surname_list = [fake.last_name() for _ in range(100)]
email_list = [fake.email() for _ in range(100)]
date_of_birth_list = [str(fake.date_of_birth(minimum_age=18, maximum_age=90)) for _ in range(100)]
age_list = [2024 - datetime.strptime(date_of_birth_list[i], "%Y-%m-%d").year for i in range(100)]

with db.cursor() as cursor:
    try:
        for i in range(100):
            cursor.execute('''INSERT INTO table1 (isim, soyisim, dateofbirth) VALUES (%s, %s, %s)                
                ''',(name_list[i], surname_list[i], date_of_birth_list[i]))
            cursor.execute('''INSERT INTO table2 (email, yas) VALUES (%s, %s)                
                ''',(email_list[i], age_list[i]))
            cursor.execute('''INSERT INTO table3 (name, age, dateofbirth) VALUES (%s, %s, %s)                
                ''',(name_list[i], age_list[i], date_of_birth_list[i]))
        db.commit()
    except psycopg2.Error as e:
        db.rollback()
        print(f"DATABASE ERROR: {e} ")



db.close()