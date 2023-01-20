import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler
from http_monitor_db import dbManager


class HttpScheduler:
    def __init__(self, dbManager: dbManager):
        self.dbManager = dbManager
        self.urls = []
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.scheduler.add_job(self.check_urls, 'interval', seconds=10)
    
    def check_urls(self):
        # check all urls in the database
        for url in self.dbManager.get_urls():
            # check if the url is already in the list
            if url["url_id"] not in self.urls:
                # add the url to the list
                self.urls.append(url["url_id"])
                # schedule the url
                self.schedule_url(url)
    
    def schedule_url(self, url, interval=10):
        # schedule the url
        self.scheduler.add_job(self.check_url, 'interval', seconds=interval, args=[url])
    
    def check_url(self, url):
        # check the url
        try:
            response = requests.request(url["method"], url["url"])
            status_code = response.status_code
        except:
            status_code = 0
        # insert the request to the database
        self.dbManager.insert_request(url["url_id"], status_code)

        # check if the url has failed requests count >= threshold
        if self.dbManager.get_failed_requests_count(url["url_id"]) >= url["threshold"]:
            # create an alert if it doesn't exist since 15 minutes
            if not self.dbManager.alert_exists_since(url["url_id"], 15):
                self.dbManager.create_alert(url["url_id"])
    
    def stop(self):
        # stop the scheduler
        self.scheduler.shutdown()