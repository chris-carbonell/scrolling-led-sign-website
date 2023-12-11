# # Overview
# API for interacting with database

# Dependencies

# general
from datetime import datetime
import os

# api
from fastapi import FastAPI, Request

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
async def get_text(tags: str = None, asc: bool = True):
    '''
    get text

    tags: tags of the text to get; string of comma-separated tags (e.g., "sports, random")
    asc: order messages aescending (i.e., True = oldest messages at the top of the queue)
    '''

    # get sql
    template = environment.get_template("get_text_where_tags.sql")
    sql = template.render(
        parsed_tags = parse_tags(tags),
        order = "ASC" if asc else "DESC"
        )

    # get text
    with connection() as conn:
        
        # get data
        curs = conn.cursor()
        curs.execute(sql)
        record = curs.fetchone()
        
        # if record exists
        if record:

            # parse record
            text_id = record[0]
            text = record[1]

            # update dt_requested
            template = environment.get_template("update_dt_requested.sql")
            sql = template.render(
                text_id = text_id,
                dt_requested = get_now_text()
                )
            curs.execute(sql)

        else:
            text = None

    return {'text': text}

## put

@app.put("/text", tags=["put"])
async def put_text(
    text: str,
    request: Request,
    source: str = "api",
    tags: str = None,
    ):
    '''
    add text to database
    '''

    # build sql
    template = environment.get_template("add_text.sql")
    sql = template.render(
        dt_entered = get_now_text(),
        client_host = request.client.host,
        source = source,
        parsed_tags = parse_tags(tags),
        text = text,
        )

    # execute
    with connection() as conn:
        curs = conn.cursor()
        curs.execute(sql)

    return

# TODO: get n texts asc/desc for checking in on people