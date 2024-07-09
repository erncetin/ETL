import psycopg2
from faker import Faker
from datetime import datetime
import mysql.connector
fake = Faker()
#queries for table creation
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

#postgresql connection
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

#mysql connection
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

#clear tables in both databases
with db_postgres.cursor() as postgres_cursor, db_mysql.cursor() as mysql_cursor:
    try:
        #clear postgresql tables
        postgres_cursor.execute('TRUNCATE TABLE table1')
        postgres_cursor.execute('TRUNCATE TABLE table2')
        postgres_cursor.execute('TRUNCATE TABLE table3')
        db_postgres.commit()

        #clear mysql tables
        mysql_cursor.execute('TRUNCATE TABLE table1')
        mysql_cursor.execute('TRUNCATE TABLE table2')
        mysql_cursor.execute('TRUNCATE TABLE table3')
        db_mysql.commit()
    except (psycopg2.Error, mysql.connector.Error) as e:
        print(f"error clearing tables: {e}")
        db_postgres.rollback()
        db_mysql.rollback()

#create tables for postgresql database
with db_postgres.cursor() as cursor:
    for query in create_table_queries:
        try:
            cursor.execute(query)
            print("creating table in postgreSQL database")
            db_postgres.commit()
        except psycopg2.Error as e:
            print(f"error while creating tables for POSTGRESQL database: {e}")



#create tables for mysql database
with db_mysql.cursor() as cursor:
    for query in create_table_queries:
        try:
            cursor.execute(query)
            print("creating table in MYSQL database")
        except mysql.connector.Error as e:
             print(f"error while creating tables for MYSQL database: {e}")
          
#dummy data
name_list = [fake.first_name() for _ in range(500)]
surname_list = [fake.last_name() for _ in range(500)]
email_list = [fake.email() for _ in range(500)]
date_of_birth_list = [str(fake.date_of_birth(minimum_age=18, maximum_age=90)) for _ in range(500)]
age_list = [2024 - datetime.strptime(date_of_birth_list[i], "%Y-%m-%d").year for i in range(500)]


#POSTGRES INSERTION
with db_postgres.cursor() as cursor:
    try:
        for i in range(500):
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

#Fetching data from postgresql and loading into mysql
with db_postgres.cursor(name="fetching_big_data") as postgres_cursor: 
    cursor.itersize = 50
    try:
        postgres_cursor.execute('''SELECT isim, soyisim, dateofbirth FROM table1
            ''')
        with db_mysql.cursor() as mysql_cursor:
            try:
                mysql_cursor.executemany('''INSERT INTO table1 (isim, soyisim, dateofbirth) VALUES (%s,%s,%s)
                    ''',(postgres_cursor.fetchall()))
                db_mysql.commit()
            except mysql.connector.Error as e:
                db_mysql.rollback()
                print(f"mysql error while inserting to table 1 {e}")
    except psycopg2.Error as e:
         print(f"postgres error {e}")
    
#Fetching data from postgresql and loading into mysql
with db_postgres.cursor(name= "fetching_big_data") as postgres_cursor: 
    cursor.itersize = 50
    try:
        postgres_cursor.execute('''SELECT email, yas FROM table2
            ''')
        with db_mysql.cursor() as mysql_cursor:
            try:
                mysql_cursor.executemany('''INSERT INTO table2 (email, yas) VALUES (%s,%s)
                    ''',(postgres_cursor.fetchall()))
                db_mysql.commit()
            except mysql.connector.Error as e:
                db_mysql.rollback()
                print(f"mysql error while inserting to table 2 {e}")
    except psycopg2.Error as e:
         print(f"postgres error {e}")

#Fetching data from postgresql and loading into mysql
with db_postgres.cursor(name="fetching_big_data") as postgres_cursor: 
    cursor.itersize = 50
    try:
        postgres_cursor.execute('''SELECT name, age, dateofbirth FROM table3
            ''')
        with db_mysql.cursor() as mysql_cursor:
            try:
                mysql_cursor.executemany('''INSERT INTO table3 (name, age, dateofbirth) VALUES (%s,%s,%s)
                    ''',(postgres_cursor.fetchall()))
                db_mysql.commit()
            except mysql.connector.Error as e:
                db_mysql.rollback()
                print(f"mysql error while inserting to table 3  {e}")
    except psycopg2.Error as e:
         print(f"postgres error {e}")


#validation of the data
with db_postgres.cursor() as postgres_cursor, db_mysql.cursor() as mysql_cursor:
    postgres_cursor.execute('''SELECT isim, soyisim, dateofbirth FROM table1 ''')
    mysql_cursor.execute('''SELECT isim, soyisim, dateofbirth FROM table1 ''')
    if mysql_cursor.fetchall() == postgres_cursor.fetchall():
        print("TABLE1 IDENTICAL")
    else:
        print("TABLE1 IS NOT IDENTICAL")
    postgres_cursor.execute('''SELECT email, yas FROM table2 ''')
    mysql_cursor.execute('''SELECT email, yas FROM table2 ''')
    if mysql_cursor.fetchall() == postgres_cursor.fetchall():
        print("TABLE2 IDENTICAL")
    else:
        print("TABLE2 IS NOT IDENTICAL")

    postgres_cursor.execute('''SELECT name, age, dateofbirth FROM table3 ''')
    mysql_cursor.execute('''SELECT name, age, dateofbirth FROM table3 ''')
    if mysql_cursor.fetchall() == postgres_cursor.fetchall():
        print("TABLE2 IDENTICAL")
    else:
        print("TABLE2 IS NOT IDENTICAL")

db_postgres.close()
db_mysql.close()