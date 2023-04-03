# Realtime Events

Repository that demo how to use Fast API Web Sockets with Kafka 

## How to run the project? 
1. Run `make setup-env`. Right now this only creates the .env based on the .env.example but you can extend it to actually pull the variables from SSM or any other place if needed
2. Update .env with the expected values to connect to Confluence. Skip it if you already did it in step one
3. Run `make docker-build`

## About the Project

- The project is based on FastAPI, WebSockets and Kafka. The configuration that is done in this project to connect to a Kafka Topic is by using Confluent. In case you are not using Confluent the project can be easily adapted since all the logic of the connection to the Kafka Topic is spllited in the environment variables and the Kafka Service
- It was built using Python 3.11

### app

The app folder is the one that contains all the code related to our Web Socket Service and the Subscription to multiple Kafka Topics

- services
    - kafka_service.py: This file contains the logic for subscribing to all the topics, deserialize the key and the value of a message from the Schema Registry
- dependencies: Folder that contains all the (dependencies)[https://fastapi.tiangolo.com/tutorial/dependencies/] defined
    - authorization.py: This file contains the dependency that will check if the organization id and user id are valid before accepting the connection
- topics: This is a folder that contains all the topics that we are going to subscribe. Each file inside of it has a function that will return the value schema and the key schema of it to later perform the deserialization
- client.py: This file contains the HTML that it can be used calling the root path in order to test the web socket testing from the UI
- main.py: This file contains the definition of the Web Socket Endpoint and the endpoint that will serve as a testing client
- settings.py: This file contains the definition of all the environment variables that will be use across the project

### Deep dive on the web socket endpoint

The goal of this section is to talk about some decicions made on web socket endpoint

- As you know most of all the web sockets frameworks needs to handle the Ping / Pong between the Client and the service to avoid having iddle connection. In order to achieve this we have to make a ping every PING_INTERVAL seconds. `ayncio.wait_for` function will fail if it can not connect to the client and this is the expected behaviour since we want to understand if client is no longer connected
- More info about this (topic)[https://github.com/tiangolo/fastapi/discussions/8280]
- uvicorn is the ASGI web server that Fast API uses, it should be who handle the ping / pong
    - Actually there are 2 parameters that you can pass
        - --ws-ping-interval
        - --ws-ping-timeout
    - The problem is that it does not work as expected since there are scenarios that the client is disconnected but the server keeps running the code
    - If you want to test this you just need to add in the docker-compose.yml `--ws websockets --ws-ping-interval 20.0 --ws-ping-timeout 60.0`

## How to Test the service?

- In order to test the service we have 2 ways

1. Open in a new Browser `http://localhost:5000`, this will use the code defined in the client.py file that will subscribe to all the topics
2. The second one and the *recommended* one is by using the `k6.js` file. This file as you already noticed use (k6)[https://k6.io/docs/using-k6/protocols/websockets/]. If you never heard about it don't worry you can find more information on the link, is a load testing framework that will allow us to write our code in js, later it will be compiled and executed in go. After performing the (installation)[https://k6.io/docs/get-started/installation] of k6 in one of the multiple ways we have, we need to run the following command `k6 run --vus 3 --duration 30s k6.js`. We can adjust the value of vus that is virtual users and the duration

## Local Development
1. `virtualenv venv-realtime-events` if your default Python version is 3.11. Use to set explicitly the version `--python=/usr/bin/python3.11`
2. `source /path/to/repo/realtime-events/venv-realtime-events/bin/activate`
3. `pip install -r requirements.txt`

*Note*: If you are using VS Code, do Ctrl + Shift + P to select as python interpreter the virtual environment it was created

## Next Steps

- As we already saw the main idea of this project was to build in 48 hours a client that can subscribe to multiple channels to receive information about their property, the project was split into 2, the Web Socket Service and a UI Dashboard. To know more about the project I invite you to see the [Medium Post](https://lucas-hartridge9.medium.com), so I will list different points that should be covered from this point in order to have the service working in a Production Environment

### Share state between service instances

- Right now the Connection to the channels is handled in Memory, in order to improve this we should have a Redis Instance that will be shared between the different instances of the Web Service. Potentially the service will be in Kubernetes so to share the state between Pods. Another alternatives than Redis can be used but from my point of view is the more reliable and simple solution we can use

### Adjust Service Logic based on Product Requirements

- As we saw right now we are subscribing to 3 Topics, receiving information from all of them. After that we are checking if the message comes from the subscribe topic / channel and if it belongs to the property that is subscribed.

#### Picking the right Parition
- For our use case unfortunately there are no partition key by organization id because of Confluent, but if in your scenario you have the right partition will help to improve the performance of the service because you will be already listening all the events that you want. In our scenario we don't have a proper partition so we need to listen all the events and perform the filtering after that, adding an extra overhead in the service

#### Allow to connect to multiple channel in one connection
- Right now our web socket service only allows to connect to 1 channel per Web Socket connection. In our use case at the end a client would need to establish 3 connection with the Web Socket Service to receive information about each channel, which has no sense because in the back we are subscribing to all the Topics. So in order to improve our service we should allow the customer to establish a connection to multiple channels and if we receive the information for their channel / topic and property we sent it back

#### Security
- As you know on Web Sockets we can not receive Headers, so we should extend the dependencies/authorization.py to validate that an user is authorize to connect to our service. One idea can be to extend the user_id query param to receive the bearer token and validate it

### Unit Test
- No much to say here, because of the rush there was no time to perform the unit test and the focus was on Integration / Load Test using k6

