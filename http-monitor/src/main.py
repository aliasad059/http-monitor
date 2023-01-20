import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from prometheus_fastapi_instrumentator import Instrumentator
from uvicorn.config import LOGGING_CONFIG

from http_monitor_db import dbManager
from http_monitor_service import httpMonitorService

load_dotenv()

http_monitor_service = httpMonitorService()
db_manager = dbManager()

app = FastAPI()
Instrumentator().instrument(app).expose(app)

@app.post("/api/users/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # authenticate user with jwt token
    return

@app.post("/api/users")
async def create_user(username: str = Form(...), password: str = Form(...)):
    # create user
    return

@app.post("/api/urls")
async def create_url(url: str = Form(...), threshold: int = Form(...)):
    # create a new url for the authenticated user (at most 20 urls per user)
    return

@app.get("/api/urls")
async def get_urls():
    # get all urls for the authenticated user
    return

@app.get("/api/urls/{url_id}")
async def get_url_status(url_id: str):
    # get the status of a url for the authenticated user
    return

@app.get("/api/alerts")
async def get_alerts():
    # get all alerts for the authenticated user
    return


def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(app, host=os.getenv("UVICORN_HOST"), port=os.getenv("UVICORN_PORT"))

if __name__ == '__main__':
    run()
