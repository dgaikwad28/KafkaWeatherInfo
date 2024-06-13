import json
import asyncio
from logging import getLogger
from logging.config import dictConfig

from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from app.database import mongo_db
from app.kafka_consumer import consume_kafka_events, send_kafka_event
from app.models import UserLocationEvent
from app.schemas import USER_SCHEMA
from app.settings import LOGGING
from app.weather_routers import get_current_weather

# logging
dictConfig(LOGGING)
api_logger = getLogger("api")

app = FastAPI()


def validate_request_body(json_data: dict, schema: dict) -> bool:
    """
    Validate the request JSON data against a given schema.

    Arguments:
    - json_data: dict - The JSON data to be validated.
    - schema: dict - The JSON schema to validate the data against.

    Returns:
    - bool: True if the data is valid according to the schema, False otherwise.

    This function validates the incoming JSON data against the specified schema and returns True if the
    data is valid. If the data is not valid, it logs an error and returns False.
    """
    try:
        # validate against the schema
        validate(instance=json_data, schema=schema)
        return True
    except ValidationError as e:
        api_logger.error(f'Invalid JSON in file: {e}')
        return False


@app.post("/weather/{user_id}",
          responses={status.HTTP_200_OK: {"model": UserLocationEvent}})
async def get_weather_info(user_id: str, request: Request):
    """
    Endpoint to get weather information based on user's location.

    Arguments:
    - user_id: str - The unique identifier for the user.
    - request: Request - The incoming request containing the user's location.

    Returns:
    - JSONResponse: The weather information based on the user's location.

    This function takes the user's location data from the request and retrieves weather information based
    on that location. It then updates the user's weather data in the database and sends a Kafka event.
    """
    body = await request.body()
    json_data = json.loads(body)

    if not validate_request_body(json_data=json_data, schema=USER_SCHEMA):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'message': 'Error importing request data'})

    weather_data = get_current_weather(lat=json_data['lat'], long=json_data['long'])
    await send_kafka_event(weather_data)

    mongo_db.update_user_data_from_email(filter_query={'user_id': user_id},
                                         data_to_update=weather_data)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=weather_data)


loop = asyncio.get_event_loop()
loop.create_task(consume_kafka_events())
