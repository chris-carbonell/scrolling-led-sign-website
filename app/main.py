# # Overview
# API for interacting with database

# Dependencies

# general
import os

# pydantic
from typing import Annotated, List
from schemas.data import TextRecord
from schemas.forms import TextForm

# api
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from api import admin, api

# app
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent, PageEvent
from fastui.forms import FormResponse, fastui_form

# data
from utils.data import connection, template_execute

# constants
from constants import *

# helpers
from utils.helpers.datetime import *
from utils.helpers.tags import *

# App
app = FastAPI(
    openapi_tags=TAGS_METADATA
)
app.include_router(admin.router, tags=["admin"])
app.include_router(api.router, tags=["api"])

# App

@app.get("/api/texts", response_model=FastUI, response_model_exclude_none=True, tags=["app|get"])
def api_texts(page: int = 1) -> list[AnyComponent]:
    '''
    tabulate text data
    '''

    # constants
    page_size = 5

    # get data
    data = template_execute("get_text_all.sql", "fetchall")

    # parse
    data = [
        TextRecord(
            dt_entered=convert_UTC(record[1]),
            dt_requested=convert_UTC(record[2]),
            client_host=record[3],
            text_source=record[4],
            text_tags=record[5],
            text=record[6],
            )
        for record in data
    ]

    return [
        c.Page(components=[
            c.Heading(text=HEADER_MAIN, level=1),
            c.Heading(text=HEADER_SUB, level=2),

            c.Heading(text="Texts!", level=3),

            c.Table[TextRecord](data=data[(page - 1) * page_size : page * page_size]),
            c.Pagination(page=page, page_size=page_size, total=len(data)),
        ])
    ]

@app.get("/api/forms/text/success", response_model=FastUI, response_model_exclude_none=True, tags=["app|get"])
def api_forms_text_success() -> list[AnyComponent]:
    '''
    when form submitted successfully, show success page
    '''
    return [
        c.Page(components=[
            c.Heading(text=HEADER_MAIN, level=1),
            c.Heading(text=HEADER_SUB, level=2),

            c.Heading(text="Success!", level=3),

            # TODO: get random success gif from giphy
            # c.Image not available in 0.2.0 (https://pypi.org/project/fastui/#history)
            # c.Image(
            #     # src="https://giphy.com/embed/a0h7sAqON67nO",
            #     src="https://cdn.drawception.com/drawings/561178/bTfogBFAxR.png",
            #     height=200,
            # ),

            c.Button(text = "Go Back", on_click = GoToEvent(url="/")),
        ])
    ]

@app.post("/api/forms/text")
async def api_forms_text(form: Annotated[TextForm, fastui_form(TextForm)]) -> FormResponse:
    '''
    when form submitted, add the text to the database
    '''

    # get dump
    form_dump = form.model_dump()

    # add to database
    template_execute(
        "add_text.sql",
        dt_entered = get_now_text(),
        client_host = None,
        source = "web_form",
        parsed_tags = None,
        text = form_dump['text'],
    )

    return FormResponse(event=GoToEvent(url="/forms/text/success"))

@app.get("/api/", response_model=FastUI, response_model_exclude_none=True, tags=["app|get"])
def api() -> list[AnyComponent]:
    '''
    root page that serves the form
    '''
    return [
        c.Page(components=[
            c.Heading(text=HEADER_MAIN, level=1),
            c.Heading(text=HEADER_SUB, level=2),

            c.Heading(text="Message Form", level=3),
            c.ModelForm[TextForm](submit_url="/api/forms/text"),
        ])
    ]

@app.get("/{path:path}", tags=["app|get"])
async def html_landing() -> HTMLResponse:
    '''
    simple HTML page which serves the React app
    comes last as it matches all paths
    '''
    return HTMLResponse(prebuilt_html(title="SLS"))