from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.dependencies import get_number_generator, get_websocket_manager
from app.api.endpoints import router
from os import getenv
from dotenv import load_dotenv


@asynccontextmanager
async def lifespan(app: FastAPI):
    number_generator = get_number_generator(get_websocket_manager())
    asyncio.create_task(number_generator.generate_numbers())
    yield


app = FastAPI(lifespan=lifespan)

load_dotenv('app/.env.secret')
SECRET_KEY = getenv('SECRET_KEY')

app.include_router(router=router)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
