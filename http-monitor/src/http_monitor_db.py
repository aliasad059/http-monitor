import psycopg2

class dbManager():
    def __init__(self, config):
        self.psql_client = psycopg2.connect(
            host=config['db_host'],
            port=config['db_port'],
            user=config['db_user'],
            password=config['db_password'],
            # database=config['db_name'],
        )
        self.psql_client.autocommit = True

        self.init_db()
        
    def close(self):
        self.psql_client.close()
    
    def init_db(self):
        cursor = self.psql_client.cursor()
        
        try:
            cursor.execute("CREATE DATABASE http_monitor")
        except psycopg2.errors.DuplicateDatabase:
            pass
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS urls (id SERIAL PRIMARY KEY, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, user_id INTEGER NOT NULL, url VARCHAR(255) NOT NULL, method VARCHAR(255) NOT NULL, threshold INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS requests (id SERIAL PRIMARY KEY, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, url_id INTEGER NOT NULL, status_code INTEGER NOT NULL, FOREIGN KEY (url_id) REFERENCES urls(id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS alerts (id SERIAL PRIMARY KEY, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, url_id INTEGER NOT NULL, FOREIGN KEY (url_id) REFERENCES urls(id))")
        
    def user_exists(self, username):
        cursor = self.psql_client.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        return cursor.fetchone() is not None
    
    def url_exists(self, user_id, url_id):
        cursor = self.psql_client.cursor()
        cursor.execute("SELECT * FROM urls WHERE user_id = %s AND id = %s", (user_id, url_id))
        return cursor.fetchone() is not None
    
    def check_password(self, username, password):
        cursor = self.psql_client.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = crypt(%s, password)", (username, password))
        return cursor.fetchone() is not None
    
    def create_user(self, username, password):
        cursor = self.psql_client.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, crypt(%s, gen_salt('bf')))", (username, password))
        return True
    
    def create_url(self, user_id, url, method, threshold):
        cursor = self.psql_client.cursor()
        cursor.execute("INSERT INTO urls (user_id, url, method, threshold) VALUES (%s, %s, %s, %s)", (user_id, url, method, threshold))
        return True

    def get_user_urls_count(self, user_id):
        cursor = self.psql_client.cursor()
        cursor.execute("SELECT COUNT(*) FROM urls WHERE user_id = %s", (user_id,))
        return cursor.fetchone()[0]
    
    def get_user_urls(self, user_id):
        cursor = self.psql_client.cursor()
        cursor.execute("SELECT * FROM urls WHERE user_id = %s", (user_id,))
        return cursor.fetchall()
    
    def get_user_url(self, user_id, url_id):
        cursor = self.psql_client.cursor()
        cursor.execute("SELECT * FROM urls WHERE user_id = %s AND id = %s", (user_id, url_id))
        return cursor.fetchone()

    def get_urls(self):
        cursor = self.psql_client.cursor()
        cursor.execute("SELECT * FROM urls")
        return cursor.fetchall()
    
    def insert_request(self, url_id, status_code):
        cursor = self.psql_client.cursor()
        cursor.execute("INSERT INTO requests (url_id, status_code) VALUES (%s, %s)", (url_id, status_code))
        return True

    def get_failed_requests_count(self, url_id):
        cursor = self.psql_client.cursor()
        cursor.execute("SELECT COUNT(*) FROM requests WHERE url_id = %s AND status_code != 200", (url_id,))
        return cursor.fetchone()[0]
    
    def get_requests_count(self, url_id):
        cursor = self.psql_client.cursor()
        cursor.execute("SELECT COUNT(*) FROM requests WHERE url_id = %s", (url_id,))
        return cursor.fetchone()[0]
    
    def create_alert(self, url_id):
        cursor = self.psql_client.cursor()
        cursor.execute("INSERT INTO alerts (url_id) VALUES (%s)", (url_id,))
        return True
        
    def alert_exists_since(self, url_id, minutes):
        cursor = self.psql_client.cursor()
        cursor.execute("SELECT * FROM alerts WHERE url_id = %s AND created_at >= NOW() - INTERVAL '%s MINUTES'", (url_id, minutes))
        return cursor.fetchone() is not None
    
    def get_alerts_since(self, user_id, minutes):
        cursor = self.psql_client.cursor()
        cursor.execute("SELECT * FROM alerts WHERE url_id IN (SELECT id FROM urls WHERE user_id = %s) AND created_at >= NOW() - INTERVAL '%s MINUTES'", (user_id, minutes))
        return cursor.fetchall()

    def get_user_id(self, username):
        cursor = self.psql_client.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        return cursor.fetchone()[0]