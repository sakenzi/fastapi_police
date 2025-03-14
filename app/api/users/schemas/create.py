from pydantic import BaseModel
from typing import Optional


class CallCreate(BaseModel):
    code: Optional[int] = None
    user_id: Optional[int] = None
    policeman_id: Optional[int] = None
    call_status_id: Optional[int] = None

    class Config():
        orm_mode = True 