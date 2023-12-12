# # Overview
# API for interacting with database

# Dependencies

# general
from datetime import datetime, date
from dateutil import tz
import os

# pydantic
from pydantic import BaseModel, Field
from typing import Annotated, List

# api
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

# app
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent, PageEvent
from fastui.forms import FormResponse, fastui_form

# data
from utils.connection import connection
import jinja2

# Constants

HEADER_MAIN = "Scrolling LED Sign"
HEADER_SUB = "poopasaurus.com"

# Schemas

class TextRecord(BaseModel):
    # TODO: the table gets Dt Entered, can we control the name of that here somehow?
    # TODO: or maybe with DisplayLookup like in the cities table in the demo
    dt_entered: datetime | None
    dt_requested: datetime | None
    client_host: str | None
    text_source: str | None
    text_tags: List[str] | None
    text: str

class TextForm(BaseModel):
    text: str

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
        return ", ".join(tags_where)
    else:
        return None

def get_now_text():
    '''
    get string of now time in UTC
    '''
    return datetime.now().strftime("%Y-%m-%d %H:%M:%SZ")  # UTC

def convert_UTC(dt_utc: str | datetime, to_zone="America/Chicago"):
    '''
    convert UTC to to_zone
    https://stackoverflow.com/questions/61831304/utc-to-cst-time-conversion-using-pytz-python-package
    '''

    # check if None
    if dt_utc is None:
        return None

    # parse time
    if isinstance(dt_utc, str):
        dt_utc = datetime.strptime(dt_utc, "%Y-%m-%d %H:%M:%SZ")

    # get zones
    from_zone = tz.gettz("UTC")
    to_zone = tz.gettz(to_zone)

    # get to_zone dt
    dt_to_zone = dt_utc.replace(tzinfo=from_zone).astimezone(to_zone)

    return dt_to_zone

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
    # api
    {"name": "api|get", "description": "api: get data"},
    {"name": "api|admin|get", "description": "api: get admin data"},
    {"name": "api|put", "description": "api: put data"},
    
    # app
    {"name": "app|get", "description": "app: get data"},
    {"name": "app|post", "description": "app: post data"},
]

## admin

@app.get("/healthcheck", tags=["api|admin|get"])
async def root():
    '''
    health check for container
    '''
    # TODO: return HTTP error if necessary table doesnt exist
    return

## get

@app.get("/text", tags=["api|get"])
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

# @app.get("/texts", tags=["api|get"])
# def get_texts():
#     '''
#     get all texts
#     '''

#     # get data
#     data = template_execute("get_text_all.sql", "fetchall")

#     return data

## put

@app.put("/text", tags=["api|put"])
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