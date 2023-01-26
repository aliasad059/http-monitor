import os

import uvicorn
from fastapi import FastAPI, Form, Request
from prometheus_fastapi_instrumentator import Instrumentator
from uvicorn.config import LOGGING_CONFIG

from http_monitor_service import httpMonitorService
from http_monitor_db import dbManager
from http_scheduler import HttpScheduler
from src.auth.auth_handler import signJWT, decodeJWT
from config import dbConfig, uvicornConfig, schedulerConfig


http_db_manager = dbManager(dbConfig)
http_monitor_service = httpMonitorService(dbManager=http_db_manager)
http_scheduler = HttpScheduler(dbManager=http_db_manager, schedulerConfig=schedulerConfig)

app = FastAPI()
Instrumentator().instrument(app).expose(app)


def get_user_id(request: Request):
    token = request.headers.get("Authorization").split(" ")[1]
    decoded_token = decodeJWT(bytes(token, "utf-8"))
    if not decoded_token:
        return False
    user_id = http_db_manager.get_user_id(decoded_token["user_id"])
    return user_id

@app.post("/api/users/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # authenticate user with jwt token
    if http_monitor_service.authenticate_user(username, password):
        signed_jwt = signJWT(username)
        return signed_jwt
    return {"message": "Invalid credentials"}

@app.post("/api/users")
async def create_user(username: str = Form(...), password: str = Form(...)):
    # create user
    if http_monitor_service.create_user(username, password):
        signed_jwt = signJWT(username)
        return signed_jwt
    return {"message": "User not created"}

@app.post("/api/urls")
async def create_url(request: Request, url: str = Form(...), method: str = Form(...), threshold: int = Form(...)):
    # create a new url for the authenticated user (at most 20 urls per user)
    user_id = get_user_id(request)
    if not user_id:
        return {"message": "Invalid token"}
    if http_monitor_service.create_url(user_id, url, method, threshold):
        return {"message": "URL created"}
    return {"message": "URL not created"}

@app.get("/api/urls")
async def get_urls(request: Request):
    user_id = get_user_id(request)
    if not user_id:
        return {"message": "Invalid token"}
    urls = http_monitor_service.get_urls(user_id)
    if urls:
        return urls
    return {"message": "No URLs found"}
    
@app.get("/api/urls/{url_id}")
async def get_url_status(url_id: str, request: Request):
    # get the status of a url for the authenticated user
    user_id = get_user_id(request)
    if not user_id:
        return {"message": "Invalid token"}
    url_status = http_monitor_service.get_url_status(user_id, url_id)
    if url_status:
        return url_status
    return {"message": "URL not found"}

@app.get("/api/alerts")
async def get_alerts(request: Request):
    # get all alerts for the authenticated user
    user_id = get_user_id(request)
    if not user_id:
        return {"message": "Invalid token"}
    alerts = http_monitor_service.get_alerts(user_id)
    if alerts:
        return alerts
    return {"message": "No alerts found"}

def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(app, host=uvicornConfig["server_host"], port=uvicornConfig["server_port"])

if __name__ == '__main__':
    run()
