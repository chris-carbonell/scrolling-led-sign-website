from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated, List

class TextRecord(BaseModel):
    # TODO: the table gets Dt Entered, can we control the name of that here somehow?
    # TODO: or maybe with DisplayLookup like in the cities table in the demo
    dt_entered: datetime | None
    dt_requested: datetime | None
    client_host: str | None
    text_source: str | None
    text_tags: List[str] | None
    text: str