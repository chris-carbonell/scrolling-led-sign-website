# Dependencies

# api
from fastapi import APIRouter
from fastapi import BackgroundTasks, HTTPException, Request

# Router
router = APIRouter()

# Endpoints

## get

@router.get("/text")
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

## put

@router.put("/text")
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