from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import time

from app.routes import router


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("trivia-api")

app = FastAPI(title="Trivia API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
async def startup():
    logger.info("Trivia API started")

@app.on_event("shutdown")
async def shutdown():
    logger.info("Trivia API shutting down")