from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import route as auth_route


app = FastAPI()

origins = [
    "http://192.168.193.31:5173",  
    "http://172.20.10.2:5173",
    "http://localhost:5173",
    "http://146.0.60.15:5173" ,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_route, prefix="/p")