from http_monitor_db import dbManager

class httpMonitorService:
    def __init__(self, dbManager: dbManager):
        self.dbManager = dbManager
        pass

    def authenticate_user(self, username, password):
        # authenticate user with jwt token

        # check if user exists
        if not self.dbManager.user_exists(username):
            return False

        # check if password is correct
        if not self.dbManager.check_password(username, password):
            return False
        
        return True
        
    def create_user(self, username, password):
        # create user
        if self.dbManager.user_exists(username):
            return False
        if self.dbManager.create_user(username, password):
            return True
        return False
    
    def create_url(self, user_id, url, method, threshold):
        # create a new url for the authenticated user (at most 20 urls per user)
        if self.dbManager.get_user_urls_count(user_id) >= 20:
            return False
        if self.dbManager.create_url(user_id, url, method, threshold):
            return True
        return False
    
    def get_urls(self, user_id):
        # get all urls for the authenticated user
        urls = []
        for url in self.dbManager.get_user_urls(user_id):
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
        if not self.dbManager.url_exists(user_id, url_id):
            return False
        
        failed_requests_count = self.dbManager.get_failed_requests_count(url_id)
        threshold = self.dbManager.get_user_url(user_id, url_id)[5]
        total_requests_count = self.dbManager.get_requests_count(url_id)

        return {
            "failed_requests_count": failed_requests_count,
            "threshold": threshold,
            "total_requests_count": total_requests_count
        }
        
    def get_alerts(self, user_id, minutes=60):
        # get all alerts for the authenticated user
        # check all the urls for the user that have failed requests count >= threshold
        
        alerts = []
        for a in self.dbManager.get_alerts_since(user_id, minutes):
            alerts.append({
                "alert_id": a[0],
                "created_at": a[1],
                "url_id": a[2],
            })
        return alerts