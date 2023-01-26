import os

import uvicorn
from fastapi import FastAPI, Form, Depends
from prometheus_fastapi_instrumentator import Instrumentator
from uvicorn.config import LOGGING_CONFIG

from http_monitor_service import httpMonitorService
from http_monitor_db import dbManager
from http_scheduler import HttpScheduler
from src.auth.auth_handler import signJWT, decodeJWT
from src.auth.auth_bearer import JWTBearer
from config import dbConfig, uvicornConfig, schedulerConfig


http_db_manager = dbManager(dbConfig)
http_monitor_service = httpMonitorService(dbManager=http_db_manager)
http_scheduler = HttpScheduler(dbManager=http_db_manager, schedulerConfig=schedulerConfig)

app = FastAPI()
Instrumentator().instrument(app).expose(app)


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
async def create_url(url: str = Form(...), method: str = Form(...), threshold: int = Form(...), dependencies=[Depends(JWTBearer())]):
    # create a new url for the authenticated user (at most 20 urls per user)
    current_user = decodeJWT(dependencies[0])
    if http_monitor_service.create_url(current_user["user_id"], url, method, threshold):
        return {"message": "URL created"}
    return {"message": "URL not created"}

@app.get("/api/urls")
async def get_urls(dependencies=[Depends(JWTBearer())]):
    # get all urls for the authenticated user
    current_user = decodeJWT(dependencies[0])
    urls = http_monitor_service.get_urls(current_user["user_id"])
    if urls:
        return urls
    return {"message": "No URLs found"}
    
@app.get("/api/urls/{url_id}")
async def get_url_status(url_id: str, dependencies=[Depends(JWTBearer())]):
    # get the status of a url for the authenticated user
    current_user = decodeJWT(dependencies[0])
    url_status = http_monitor_service.get_url_status(current_user["user_id"], url_id)
    if url_status:
        return url_status
    return {"message": "URL not found"}

@app.get("/api/alerts")
async def get_alerts(dependencies=[Depends(JWTBearer())]):
    # get all alerts for the authenticated user
    current_user = decodeJWT(dependencies[0])
    alerts = http_monitor_service.get_alerts(current_user["user_id"])
    if alerts:
        return alerts
    return {"message": "No alerts found"}

def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(app, host=uvicornConfig["server_host"], port=uvicornConfig["server_port"])

if __name__ == '__main__':
    run()
