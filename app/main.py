# # Overview
# frontend/backend for interacting with database

# Dependencies

# api
from fastapi import FastAPI
from api import admin, api
from www import www

# constants
from constants import TAGS_METADATA

# App
app = FastAPI(
    openapi_tags=TAGS_METADATA
)
app.include_router(admin.router, include_in_schema=False)
app.include_router(api.router, tags=["api"])
app.include_router(www.router, tags=["www"])