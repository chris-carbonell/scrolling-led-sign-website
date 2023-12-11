# # Overview
# API for interacting with database

# Dependencies

# general
from datetime import datetime
import os

# api
from fastapi import BackgroundTasks, FastAPI, Request

# data
from utils.connection import connection
import jinja2

# App

# app
app = FastAPI()

# Helper Funcs

def parse_tags(tags: str | None):
    '''
    convert "a,b, c" to "'a', 'b', 'c'"
    for use with ARRAY[]
    '''
    if tags:
        tags_where = ["'" + tag.strip() + "'" for tag in tags.split(",")]
        return ', '.join(tags_where)
    else:
        return None

def get_now_text():
    '''
    get string of now time
    '''
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def template_execute(path_template: str, fetch: str = None, **kwargs):
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

        # fetch
        if fetch:
            if fetch == "fetchone":
                r = curs.fetchone()
            elif fetch == "fetchall":
                r = curs.fetchall()
            else:
                raise AttributeError(f"fetch ({fetch}) not supported")
            return r

    return

# jinja

environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader("./templates")
)

# endpoints

## metadata
tags_metadata = [
    {"name": "admin", "description": "admin tools"},
    {"name": "get", "description": "get data"},
    {"name": "put", "description": "put data"},
]

## admin

@app.get("/healthcheck", tags=["admin"])
async def root():
    '''
    health check for container
    '''
    # TODO: return HTTP error if necessary table doesnt exist
    return

## get

@app.get("/text", tags=["get"])
def get_text(background_tasks: BackgroundTasks, tags: str = None, asc: bool = True):
    '''
    get text

    tags: tags of the text to get; string of comma-separated tags (e.g., "sports, random")
    asc: order messages aescending (i.e., True = oldest messages at the top of the queue)
    '''

    # get data
    record = template_execute(
        "get_text_where_tags.sql",
        "fetchone",
        parsed_tags = parse_tags(tags),
        asc = asc
        )

    # parse
    
    # record exists
    if record:
        
        # parse
        text_id = record[0]
        text = record[1]

        # update dt_requested in background task
        background_tasks.add_task(
            template_execute,
            "update_dt_requested.sql",
            text_id = text_id,
            dt_requested = get_now_text()
            )
    
    # no record exists
    else:
        text = None

    return {'text': text}

@app.get("/texts", tags=["get"])
def get_texts():
    '''
    get all texts
    '''

    # get data
    data = template_execute("get_text_all.sql", "fetchall")

    return data

## put

@app.put("/text", tags=["put"])
def put_text(
    text: str,
    request: Request,
    source: str = "api",
    tags: str = None,
    ):
    '''
    add text to database
    '''

    # update dt_requested
    template_execute(
        "add_text.sql",
        dt_entered = get_now_text(),
        client_host = request.client.host,
        source = source,
        parsed_tags = parse_tags(tags),
        text = text,
    )

    return