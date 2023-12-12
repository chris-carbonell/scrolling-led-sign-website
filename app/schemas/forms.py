from pydantic import BaseModel, Field

class TextForm(BaseModel):
    text: str