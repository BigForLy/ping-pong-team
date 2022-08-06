# ping-pong-team

Two applications based on Webframework FastAPI, both consumer and producer. Applications track messages from Kafka through specific tags, each for their application. Applications exchange messages in this way playing ping-pong, to start the game send a request to the address of one of the applications `/api/ping/`.

## Stack

- FastAPI
- aiokafka
- uvicorn
- gunicorn

## Infrastructure

- FastAPI first
- FastAPI second
- Zookeeper
- Kafka
- Kafdrop

## How to use

### Using Docker Compose 
You will need Docker installed to follow the next steps. To create and run the image use the following command:

```bash
> docker-compose up --build
```

The configuration will create a cluster with 5 containers. No .env file needed, only docker-compose environment.
