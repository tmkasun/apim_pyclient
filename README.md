# This repository contains a Python Client for playing with WSO2 API Manager REST API and a dummy HTTP(s) and WebSocket server for handling/monitoring requests

I wrote this simple python client to make it easy to create , delete , update lifecycle states of an API for testing purposes.

# How to get swagger definitions for Store Publisher REST APIS ?

Start [WSO2 API Manager](http://wso2.com/api-management/) server. You can get the swagger definitions for store and publisher REST APIs in following locations.

- Store : https://localhost:9443/api/am/store/v1.0/apis/swagger.json
- Publisher : https://localhost:9443/api/am/publisher/v1.0/apis/swagger.json

You need to change the `API version` , `hostname` and `port` accordingly.

# Create test artifacts

- Delete existing APIs
- Delete existing Endpoints
- Create new APIs
- Create new Global endpoints
- Publish newly created APIs
- Create new Store Application
- Delete all existing users (Except admin)
- Create new users

# Echo HTTP(S) server

How to start the simple HTTP server

```bash
python3 simple_endpoint.py
```

## Available services with echo server

- Support Digest Auth
  - Send a request with `digestme` word in anywhere in the request path
- Basic Auth header decode
- CORS request handler
- Dump payload in `POST`, `PUT` or `PATCH` requests
- Dump all the headers and return them as JSON in response body
- Delay (mimic backend latency) response by setting the `kdelay` (seconds) query parameter in the request i:e http://localhost:8000/apis?kdelay=2.5
- Response with supported content types (`application/xml` or `application/json`). Honor the `accept` header if present
- Return sample file when requested with available sample files extensions in `mock_servers/resources/` directory
  - Example: localhost:8000/apis/send/me/a.pdf will return python.pdf file in `mock_servers/resources/` with content-type header as `application/pdf`
  - If want to add support to new extension, put the file to `mock_servers/resources/` i:e `my_sample.extension` and make a request like localhost:8000/apis/send/my/sample.extension , It will return the `my_sample.extension` file with `application/{extension}` in the `content-type` header

# Websocket Echo server

How to start the simple HTTP endpoint server

```bash
python3 simple_websocket.py
```

## What can I do with Simple websocket server

Simple service to monitor WS initialization flow

- See the initial handshake HTTP request
- Dump websocket frame content
- Reply to WS message
