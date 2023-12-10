# Dependencies

# testing
import pytest

# general
import os

# app
from utils.connection import connection

# Tests

def test_env_vars():
    '''
    GIVEN   nothing
    WHEN    nothing
    THEN    environment variables exist and are not blank
    '''

    def verify_var(var):
        return len(var) > 0

    assert verify_var(os.environ['POSTGRES_HOST'])
    assert verify_var(os.environ['POSTGRES_PORT'])
    assert verify_var(os.environ['POSTGRES_DB'])
    assert verify_var(os.environ['POSTGRES_USER'])
    assert verify_var(os.environ['POSTGRES_PASSWORD'])

def test_conn():
    '''
    GIVEN   environment variables for database connection exist
    WHEN    a connection initialized
    THEN    the connection can provide info on the database
    '''

    # get default conn and cursor
    with connection() as conn:
        curs = conn.cursor()
        curs.execute("SELECT version();")
        record = curs.fetchone()
        ver = record[0]

    assert ver is not None
    assert "PostgreSQL" in ver