from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
from datetime import datetime
from model.model import Statement
from fastapi import HTTPException
from core.config import settings


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

