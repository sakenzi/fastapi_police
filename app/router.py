from fastapi import APIRouter
from app.api.auth.auth import router as auth_user_router
from app.api.auth.admin_auth import router as auth_admin_router

route = APIRouter()

route.include_router(auth_user_router, prefix="", tags=["UserAuthentication"])
route.include_router(auth_admin_router, prefix="", tags=["AdminAuthentication"])