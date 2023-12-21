# # Overview
# frontend/backend for interacting with database

# Dependencies

# general
import logging
import os

# api
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api import admin, api

# constants
from constants import TAGS_METADATA

# Logging
logger = logging.getLogger(__name__)

# App
app = FastAPI(
    openapi_tags=TAGS_METADATA
)

# Routers
app.include_router(admin.router, include_in_schema=False)
app.include_router(api.router, tags=["api"])

# Endpoints

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')