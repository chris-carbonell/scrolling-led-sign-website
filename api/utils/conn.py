# Dependencies

# general
import os

# data
import psycopg2

# Classes

class connection(psycopg2._psycopg.connection):
    '''
    connection to database
    just pull default connection details from environment variables
    '''

    def __init__(
        self, 
        host:str = os.environ['POSTGRES_HOST'], 
        port:str = os.environ['POSTGRES_PORT'], 
        database:str = os.environ['POSTGRES_DB'], 
        user:str = os.environ['POSTGRES_USER'], 
        password:str = os.environ['POSTGRES_PASSWORD'],
        ):

        # get dsn
        dsn = psycopg2.extensions.make_dsn(host=host, port=port, database=database, user=user, password=password)

        # create conn
        super().__init__(dsn=dsn)