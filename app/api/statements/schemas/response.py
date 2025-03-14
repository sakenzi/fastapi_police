from pydantic import BaseModel
from typing import Optional


class StatementResponse(BaseModel):
    text: str

