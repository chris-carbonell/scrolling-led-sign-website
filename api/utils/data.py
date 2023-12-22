# Dependencies

# general
import os

# data
import jinja2
import psycopg2

# Setup

# jinja
environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader("./templates")
)

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

# Funcs

def template_execute(path_template: str, **kwargs):
    '''
    render template and execute
    '''

    # render template
    template = environment.get_template(path_template)
    sql = template.render(**kwargs)

    # get data
    with connection() as conn:
        curs = conn.cursor()
        curs.execute(sql)
        
        # fetch if exists
        if curs.description:
            r = curs.fetchall()  # list of tups
            column_names = [desc[0] for desc in curs.description]

            # convert to list of dicts
            r = [{col: obj for col, obj in zip(column_names, row)} for row in r]
        
        else:
            return  # no data to return
    
    return r