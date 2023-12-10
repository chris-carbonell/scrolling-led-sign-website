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

@app.get("/")
async def root():
    return {"message": "Hello World"}
