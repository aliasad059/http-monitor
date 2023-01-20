from http_monitor_db import dbManager

class httpMonitorService:
    def __init__(self):
        pass

    def authenticate_user(self, username, password):
        # authenticate user with jwt token

        # check if user exists
        if not dbManager.user_exists(username):
            return False

        # check if password is correct
        if not dbManager.check_password(username, password):
            return False
        
        return True
        
    def create_user(self, username, password):
        # create user
        if dbManager.user_exists(username):
            return False
        if dbManager.create_user(username, password):
            return True
        return False
    
    def create_url(self, user_id, url, threshold):
        # create a new url for the authenticated user (at most 20 urls per user)
        if dbManager.get_urls_count(user_id) >= 20:
            return False
        if dbManager.create_url(user_id, url, threshold):
            return True
        return False
    
    def get_urls(self, user_id):
        # get all urls for the authenticated user
        urls = []
        for url in dbManager.get_urls(user_id):
            urls.append({
                "url_id": url[0],
                "url": url[3],
                "threshold": url[5],
                "method": url[4],
                "created_at": url[1]
            })
        if len(urls) == 0:
            return False
        return urls
    
    def get_url_status(self, user_id, url_id):
        # get the status of a url for the authenticated user
        if not dbManager.url_exists(user_id, url_id):
            return False
        
        failed_requests_count = dbManager.get_failed_requests_count(user_id, url_id)
        threshold = dbManager.get_threshold(user_id, url_id)
        total_requests_count = dbManager.get_requests_count(user_id, url_id)

        return {
            "failed_requests_count": failed_requests_count,
            "threshold": threshold,
            "total_requests_count": total_requests_count
        }
        
    def get_alerts(self, user_id):
        # get all alerts for the authenticated user
        # check all the urls for the user that have failed requests count >= threshold
        urls = dbManager.get_urls(user_id)
        alerts = []
        for url in urls:
            failed_requests_count = dbManager.get_failed_requests_count(user_id, url["url_id"])
            if failed_requests_count >= url["threshold"]:
                alerts.append({
                    "url": url["url"],
                    "failed_requests_count": failed_requests_count
                })
        if len(alerts) == 0:
            return False
        return alerts