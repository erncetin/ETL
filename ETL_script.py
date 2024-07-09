import psycopg2
from faker import Faker
from datetime import datetime
import mysql.connector
fake = Faker()

try:
        db_postgres = psycopg2.connect(
            database = "db_postgres",
            user = "root",
            password = "root",
            host = "host_postgres",
            port = "5432"
        )
        print("POSTGRES BAGLANDI")
except psycopg2.Error as e:
        print(f"failed to connect to database: {e}")

try:
    db_mysql = mysql.connector.connect(
    host="host_mysql",
    user="root",
    password="root",
    database="db_mysql",
    port= "3306"
    )
    print("MYSQL BAGLANDI")

except mysql.connector.Error as e:
     print(f"MYSQL DATABASE ERROR: {e}")


create_table_queries = [#queries for postgres database
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
with db_postgres.cursor() as cursor:
    for query in create_table_queries:
        try:
            cursor.execute(query)
            print("creating table in postgreSQL database")
            db_postgres.commit()
        except psycopg2.Error as e:
            print(f"error while creating tables for POSTGRESQL database: {e}")#commit the queries for postgres database

with db_mysql.cursor() as cursor:
    for query in create_table_queries:
        try:
            cursor.execute(query)
            print("creating table in MYSQL database")
        except mysql.connector.Error as e:
             print(f"error while creating tables for MYSQL database: {e}")#commit the queries for mysql database
          



name_list = [fake.first_name() for _ in range(100)]
surname_list = [fake.last_name() for _ in range(100)]
email_list = [fake.email() for _ in range(100)]
date_of_birth_list = [str(fake.date_of_birth(minimum_age=18, maximum_age=90)) for _ in range(100)]
age_list = [2024 - datetime.strptime(date_of_birth_list[i], "%Y-%m-%d").year for i in range(100)]# dummy schema



with db_postgres.cursor() as cursor:
    try:
        for i in range(100):
            cursor.execute('''INSERT INTO table1 (isim, soyisim, dateofbirth) VALUES (%s, %s, %s)                
                ''',(name_list[i], surname_list[i], date_of_birth_list[i]))
            cursor.execute('''INSERT INTO table2 (email, yas) VALUES (%s, %s)                
                ''',(email_list[i], age_list[i]))
            cursor.execute('''INSERT INTO table3 (name, age, dateofbirth) VALUES (%s, %s, %s)                
                ''',(name_list[i], age_list[i], date_of_birth_list[i]))
        db_postgres.commit()
    except psycopg2.Error as e:
        db_postgres.rollback()
        print(f"DATABASE ERROR: {e} ")



db_postgres.close()