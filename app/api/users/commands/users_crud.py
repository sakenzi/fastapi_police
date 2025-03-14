import logging
from app.api.users.schemas.response import UserResponse
from sqlalchemy import select
from model.model import User, SessionCall
from fastapi import HTTPException
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from asterisk.manager import Manager
from app.api.users.schemas.create import CallCreate
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def get_user_by_email(db: AsyncSession, email: str) -> User:
    stmt = select(User).filter(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"Profile retrieved for user id: {email}")
    return user

'''Эндпоинт для IP-телефоний'''
async def initiate_call(from_ext: str, to_ext: str):
    manager = Manager()
    try:
        manager.connect('localhost', port=5038)
        manager.login('admin', 'adminpass')
        response = manager.originate(
            channel=f"PJSIP/{from_ext}",
            exten=to_ext,
            context="internal",
            priority=1,
            caller_id=from_ext,
            timeout=30000
        )
        print(f"Full originate response: {response.response}")

        manager.close()
        first_line = response.response[0].lower()  
        if "response: success" in first_line:
            return {"status": "success", "message": f"Call initiated from {from_ext} to {to_ext}"}
        else:
            raise HTTPException(status_code=500, detail=f"Originate failed: {response.response}")
    except Exception as e:
        manager.close()
        print(f"Error in originate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to initiate call: {str(e)}")
    

async def create_call(call: CallCreate, db: AsyncSession):
    new_call = SessionCall(
        code=call.code,
        user_id=call.user_id,
        policeman_id=call.policeman_id,
        call_status_id=call.call_status_id,
        created_at=datetime.utcnow()
    )    

    try:
        db.add(new_call)
        await db.commit()
        await db.refresh(new_call)
        return new_call

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create session call: {str(e)}")
