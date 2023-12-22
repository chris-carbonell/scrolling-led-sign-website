# Dependencies

# api
from fastapi import APIRouter
from fastapi import BackgroundTasks, HTTPException, Request

# data
from utils.data import template_execute

# helpers
from utils.helpers.datetime import *
from utils.helpers.tags import *

# Router
router = APIRouter()

# Endpoints

## get

@router.get("/text", name="get text from database")
def get_text(background_tasks: BackgroundTasks, tags: str = None, asc: bool = True):
    '''
    get text

    tags: tags of the text to get; string of comma-separated tags (e.g., "sports, random")
    asc: order messages aescending (i.e., True = oldest messages at the top of the queue)
    '''

    # get data
    data = template_execute(
        "get_text_where_tags.sql",
        parsed_tags = parse_tags(tags),
        asc = asc
        )

    # parse
    
    # data exists
    if data:
        
        # parse
        record = data[0]
        text_id = record['text_id']
        text = record['text']

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

@router.get("/texts", name="get all texts from the database")
def get_texts(tags: str = None, asc: bool = True, limit: int = None):
    '''
    get all texts

    tags: tags of the text to get; string of comma-separated tags (e.g., "sports, random")
    asc: order messages aescending (i.e., True = oldest messages at the top of the queue)
    '''

    # get data
    data = template_execute(
        "get_text_all.sql",
        "fetchall",
        parsed_tags = parse_tags(tags),
        asc = asc,
        limit = limit
        )

    return data

## put

@router.put("/text", name="add text to the database")
def put_text(
    text: str,
    request: Request,
    source: str = "api",
    tags: str = None,
    ):
    '''
    add text to the database
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