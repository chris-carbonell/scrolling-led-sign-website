# # Overview
# API for interacting with database

# Dependencies

# general
import os

# api
from fastapi import FastAPI

# data
import psycopg2
from psycopg2 import Error

# app
app = FastAPI()

# endpoints

@app.get("/healthcheck")
async def root():
    '''
    health check for container
    '''
    return