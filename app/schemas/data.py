from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated, List

class TextRecord(BaseModel):
    dt_entered: datetime | None = Field(title="dt_entered")
    dt_requested: datetime | None = Field(title="dt_requested")
    client_host: str | None = Field(title="client_host")
    text_source: str | None = Field(title="text_source")
    text_tags: List[str] | None = Field(title="text_tags")
    text: str = Field(title="text")