from dotenv import load_dotenv
import os

load_dotenv()

# db config
dbConfig = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user":
    os.getenv("DB_USER"),
    "password":
    os.getenv("DB_PASSWORD"),
    "database":
    os.getenv("DB_NAME"),
}

# server config
uvicornConfig = {
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
}

# scheduler config

schedulerConfig = {
    'request_interval': os.getenv("REQUEST_INTERVAL"), # in seconds
    'push_alert_interval': os.getenv("PUSH_ALERT_INTERVAL"), # in minutes
    'refresh_urls_interval': os.getenv("REFRESH_URLS_INTERVAL"), # in seconds
}