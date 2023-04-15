import mysql.connector
import timeit
import logging

from faker import Faker

logging.basicConfig(level=logging.INFO, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

test_query = "SELECT name FROM users ORDER BY birth_year DESC LIMIT 50000"

database_connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='root_pass',
    database='log_demo'
)

database_connection_cursor = database_connection.cursor()


def run_select():
    database_connection_cursor.execute(test_query)
    database_connection_cursor.fetchall()


def run_test(repeats, runs, long_query_time):
    logging.info(f"SET GLOBAL long_query_time = {long_query_time}")
    database_connection_cursor.execute(f"SET GLOBAL long_query_time = {long_query_time}")
    database_connection.commit()
    result = timeit.Timer(run_select).repeat(repeat=repeats, number=runs)
    logging.info(f"Result: {result[0] / number_run}s, {result[1] / runs}s, {result[2] / runs}s")


logging.info("Preparation for demo")
table_query = """
CREATE TABLE IF NOT EXISTS users
(
    id         INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name       varchar(255) NOT NULL,
    birth_year DATE         NOT NULL,
    email      varchar(255) NOT NULL,
    address    varchar(255) NOT NULL
) ENGINE = InnoDB;
"""
database_connection_cursor.execute(table_query)
database_connection.commit()
logging.info("Users table was created for test.")

fake = Faker()
users = []
for _ in range(500000):
    users.append([fake.name(), fake.date(), fake.email(), fake.address()])

user_query = "INSERT INTO users (name, birth_year, email, address) VALUES (%s, %s, %s, %s)"
database_connection_cursor.executemany(user_query, users)
database_connection.commit()
logging.info("Users table was enriched by test data (500000 rows)")

repeat_run = 3
number_run = 10

logging.info(f"Run SQL queries with different long_query_time property. Repeats: {repeat_run}, executions: {number_run}")
logging.info(f"Query: {test_query}")

run_test(repeat_run, number_run, 10)
run_test(repeat_run, number_run, 1)
run_test(repeat_run, number_run, 0)

database_connection.close()
