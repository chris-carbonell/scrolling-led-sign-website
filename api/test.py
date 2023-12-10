# # Overview
# connect to db

# Dependencies

# general
import os

# api
import fastapi

# data
import psycopg2
from psycopg2 import Error

# connect to db

try:
    # Connect to an existing database
    connection = psycopg2.connect(user=os.environ['POSTGRES_USER'],
                                  password=os.environ['POSTGRES_PASSWORD'],
                                  host=os.environ['POSTGRES_HOST'],
                                  port=os.environ['POSTGRES_PORT'],
                                  database=os.environ['POSTGRES_DB'])

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")