# # Overview
# frontend/backend for interacting with database

# Dependencies

# general
import logging
import os

# api
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from api import admin, api

# constants
from constants import TAGS_METADATA

# Logging
logger = logging.getLogger(__name__)

# App
app = FastAPI(
    openapi_tags=TAGS_METADATA
)

# CORS
# domain = os.environ['DOMAIN']
# origins = [
#     f"http://{domain}",
#     f"https://{domain}",
# ]
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(admin.router, include_in_schema=False)
app.include_router(api.router, tags=["api"])

# Endpoints

@app.get("/")
async def docs_redirect():
    return RedirectResponse(url='/docs')