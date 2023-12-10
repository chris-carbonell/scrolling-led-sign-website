# # Overview
# API for interacting with database

# Dependencies

# general
import os

# api
from fastapi import FastAPI

# data
from utils.conn import connection

# app
app = FastAPI()

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
async def get_text(types: str = None, asc: bool = True):
    '''
    get text

    types: type of text to get; string of comma-separated types (e.g., "sports, random")
    asc: order messages aescending (i.e., True = oldest messages at the top of the queue)
    '''

    # get sql
    sql = "SELECT text FROM texts"
    if types:
        sql += f" WHERE type IN ({types})"
    sql += " ORDER BY dt_entered"
    if asc:
        sql += " ASC"
    else:
        sql += " DESC"
    sql += ";"

    # get text
    with connection() as conn:
        curs = conn.cursor()
        curs.execute(sql)
        record = curs.fetchone()
        text = record[0]

    return {'text': text}

# TODO: put to add text (for front end)
# TODO: get n texts asc/desc for checking in on people