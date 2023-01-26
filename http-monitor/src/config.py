from dotenv import load_dotenv
import os

load_dotenv()

# db config
dbConfig = {
    "db_host": os.getenv("DB_HOST"),
    "db_port": os.getenv("DB_PORT"),
    "db_user": os.getenv("DB_USER"),
    "db_password": os.getenv("DB_PASSWORD"),
    "db_name": os.getenv("DB_NAME"),
}

# server config
uvicornConfig = {
    "server_host": os.getenv("SERVER_HOST"),
    "server_port": int(os.getenv("SERVER_PORT")),
}

# scheduler config

schedulerConfig = {
    'request_interval': int(os.getenv("REQUEST_INTERVAL")), # in seconds
    'push_alert_interval': int(os.getenv("PUSH_ALERT_INTERVAL")), # in minutes
    'refresh_urls_interval': int(os.getenv("REFRESH_URLS_INTERVAL")), # in seconds
}