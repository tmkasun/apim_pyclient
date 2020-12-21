#!/usr/bin/env python3
import asyncio
import ssl
import websockets
from websockets import WebSocketServerProtocol

# Simple WS server for testing APIM WS APIs

"""
http://websockets.readthedocs.io/en/stable/deployment.html#port-sharing
"""


class SimpleServer(WebSocketServerProtocol):
    async def process_request(self, path, request_headers):
        print("TMKASUN:WS:HANDSHAKE:HTTP <<<< path ={path}".format(path=path))
        for name in request_headers:
            print("TMKASUN:WS:HANDSHAKE:HTTP <<<< {name} ---- {header}".format(
                name=name, header=request_headers[name]))
        # return http.HTTPStatus.SWITCHING_PROTOCOLS, [], b'OK\n'
        return None


async def simpleWS(websocket, path):
    # http://websockets.readthedocs.io/en/stable/cheatsheet.html#keeping-connections-open
    while True:
        try:
            name = await asyncio.wait_for(websocket.recv(), timeout=20)
        except asyncio.TimeoutError:
            # No data in 20 seconds, check the connection.
            try:
                pong_waiter = await websocket.ping()
                await asyncio.wait_for(pong_waiter, timeout=10)
            except asyncio.TimeoutError:
                # No response to ping in 10 seconds, disconnect.
                break
        else:
            print("TMKASUN:WS:WIRE <<<< {name}".format(name=name))
            reply = "Hello {name}".format(name=name)
            await websocket.send(reply)
            print("TMKASUN:WS:WIRE >>>> {reply}".format(reply=reply))


def main():
    secured = False
    host = "localhost"
    port = 8005
    ssl_context = None
    scheme = "ws"
    if secured:
        scheme = "wss"
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        cert_path = 'certificates/public.crt'
        ssl_context.load_cert_chain(cert_path)
        print("Starting simple Websocket Server with TLS")
    else:
        print("Starting simple Websocket Server")
    start_server = websockets.serve(
        simpleWS, host, port, create_protocol=SimpleServer, ssl=ssl_context)
    asyncio.get_event_loop().run_until_complete(start_server)
    print("Simple Websocket Server started!\nURL => {scheme}://{host}:{port}".format(
        host=host, port=port, scheme=scheme))
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
