# Weather Service Application

This is a weather service application that retrieves weather information based on user location, stores the data in a MongoDB database, and sends Kafka events for further processing.


## Assumptions
- Usage of mongodb
- Usage aiokafka


## Features

- Retrieves weather information based on user's location
- Validates incoming JSON data against a specified schema
- Stores user's weather data in a MongoDB database
- Sends Kafka events for further processing

## Tech Stack

- FastAPI: Web framework for building APIs with Python
- Kafka: Distributed streaming platform
- MongoDB: NoSQL database program
- JSONSchema: Used for validating JSON data
- Pydantic: Data validation and settings management using Python type annotations

## Installation

1. Clone the repository:
  ```
  cp env/example.env env/.env
  ```
2. Install dependencies:
  ```
  pip install -r .\requirements\requirements.txt
  ```
3. Rename `example.env` to `.env` and update the configuration variables as per your requirements.

## Running the Application

Run the FastAPI app using the following command:
```bash
uvicorn app.main:app --reload
```

## Next Steps

- Add authentication 
- Add test cases 
- Integrate swagger
- Dockerize
- Github pipelines
- Configure Nginx

## Resources
- https://medium.com/@arturocuicas/fastapi-and-apache-kafka-4c9e90aab27f
- https://pypi.org/project/aiokafka/
- CHATGPT for docstrings and for some kafka functionalities
  - Certainly! In the provided example, we can modify the usage of Kafka with async and await, making use of the `aiokafka` library, which is the async version of Kafka client for Python.

      Here's an updated example using async and await with the `aiokafka` library:
    
      ```python
      # main.py
    
      import json
      from fastapi import FastAPI, HTTPException
      from aiokafka import AIOKafkaProducer
    
      app = FastAPI()
    
      # Kafka producer configuration
      KAFKA_BOOTSTRAP_SERVERS = 'kafka_broker1:9092,kafka_broker2:9092'  # Replace with actual Kafka broker addresses
      KAFKA_TOPIC = 'user_location_events'
    
      async def send_kafka_event(event_data: dict):
          producer = AIOKafkaProducer(
              bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
          )
          await producer.start()
        
          value = json.dumps(event_data).encode('utf-8')
          await producer.send_and_wait(KAFKA_TOPIC, value)
        
          await producer.stop()
    
      # API endpoint to send user location events to Kafka
      @app.post("/send-location-event/{user_id}")
      async def send_location_event(user_id: str, lat: float, lon: float):
          event_data = {
              "user_id": user_id,
              "lat": lat,
              "lon": lon
          }
          await send_kafka_event(event_data)
          return {"message": "Location event sent to Kafka"}
    
      if __name__ == "__main__":
          import uvicorn
          uvicorn.run(app, host="0.0.0.0", port=8000)
      ```
    
      In this modified example, the `aiokafka` library is used to create an asynchronous Kafka producer. The `send_kafka_event` function is defined as asynchronous and uses `await` to asynchronously send the event to the Kafka topic. The API endpoint `send-location-event` now uses the `async` keyword, and the `await` keyword is used to call the `send_kafka_event` function.
    
      By making these modifications, the Kafka event production in the FastAPI service is now handled asynchronously using the `aiokafka` library, providing improved performance and scalability for serving events to Kafka.