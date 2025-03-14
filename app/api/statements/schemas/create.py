from pydantic import BaseModel
from typing import Optional


class StatementCreate(BaseModel):
    text: Optional[str] = None
