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

# App

# app
app = FastAPI()

# Helper Funcs

def parse_tags(tags: str):
    '''
    convert "a,b, c" to "'a', 'b', 'c'"
    for use with ARRAY[]
    '''
    tags_where = ", ".join(["'" + tag.strip() + "'" for tag in tags.split()])
    return ', '.join([tags_where])

def get_now_text():
    '''
    get string of now time
    '''
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
    sql = "SELECT \n\ttext_id\n\t, text \nFROM texts"
    sql += "\nWHERE dt_requested IS NULL"
    if tags:
        sql += f"\n\tAND text_tags @> ARRAY[{parse_tags(tags)}]"
    sql += "\nORDER BY dt_entered"
    if asc:
        sql += " ASC"
    else:
        sql += " DESC"
    sql += ";"

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
            sql = f"UPDATE texts SET dt_requested = '{get_now_text()}' WHERE text_id = {text_id}"
            curs.execute(sql)

        else:
            text = None

    return {'text': text}

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
    # TODO: shoudl this be handled by sqlalchemy? pydantic?
    sql = "INSERT INTO texts (dt_entered, dt_requested, client_host, text_source, text_tags, text) VALUES ("
    sql += "'" + get_now_text() + "', "  # dt_entered
    sql += "NULL, "  # dt_requested
    sql += "'" + request.client.host + "', "  # client_host
    sql += "'" + source + "', "  # text_source
    sql += f"ARRAY[{parse_tags(tags)}]" if tags else "NULL, "
    sql += "'" + text + "');"

    # execute
    with connection() as conn:
        curs = conn.cursor()
        curs.execute(sql)

    return

# TODO: get n texts asc/desc for checking in on people