from pydantic import BaseModel
from typing import Optional
from enum import Enum


class CallStatus(str, Enum):
    INITIATED = 'инициированный'
    ONGOING = 'текущий'
    COMPLETED = 'завершенный'
    MISSED = 'пропущенный'
    REJECTED = 'отклоненный'

class CallCreate(BaseModel):
    code: Optional[int] = None
    user_id: Optional[int] = None
    policeman_id: Optional[int] = None
    status: CallStatus
    