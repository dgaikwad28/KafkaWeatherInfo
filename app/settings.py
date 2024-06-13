import json
import os
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

load_dotenv(os.path.join(ROOT_DIR, "env", ".env"))


def logging_config():
    file_path = os.path.join(ROOT_DIR, 'logging' + '.json')
    if not file_path:
        raise ValueError('Improperly Configured')
    try:
        with open(file_path) as fd:
            content = fd.read()
            return json.loads(content)
    except Exception:
        raise ValueError('Improperly Configured')


LOGGING = logging_config()

# Kafka
KAFKA_SERVER = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_GROUP_ID = 'weather_service_group'
KAFKA_TOPIC = 'user_location_topic'

# DB
MONGO_URI = os.environ.get("MONGO_URI")

# OpenWeatherMap creds
OWM_BASE_URL = os.environ.get("OPENWEATHERMAP_URL")
OWM_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY")
