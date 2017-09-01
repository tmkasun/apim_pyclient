import json
from http import server, HTTPStatus
import socketserver


class EndpointHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.common_handler()

    def do_POST(self):
        self.common_handler()

    def do_PUT(self):
        self.common_handler()

    def do_OPTIONS(self):
        requested_headers = self.headers.get("Access-Control-Request-Headers")
        requested_methods = self.headers.get("Access-Control-Request-Method")
        requested_origin = self.headers.get("Origin")
        self.send_header("Access-Control-Allow-Origin", requested_origin)
        self.send_response(HTTPStatus.OK)
        # Pseudo code
        # If requested_origin in allowed origin(s) or in configuration:
        #   Add domain to Access-Control-Allow-Origin response header
        self.send_header("Access-Control-Allow-Headers", requested_headers)
        self.send_header("Access-Control-Allow-Methods", requested_methods)
        # Pseudo code
        # If requested_headers in safelisted-request-headers #https://fetch.spec.whatwg.org/#cors-safelisted-request-header
        # Append header to Access-Control-Allow-Headers header value
        self.end_headers()
        request_headers = {}
        for header in self.headers._headers:
            request_headers[header[0]] = header[1]
        self.wfile.write("")

    def common_handler(self):
        # self.send_response(HTTPStatus.FORBIDDEN)
        self.send_response(HTTPStatus.OK)
        print(self.path)
        self.send_header("Content-type", "application/json")
        requested_origin = self.headers.get("Origin")
        self.send_header("Access-Control-Allow-Origin", requested_origin)
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Set-Cookie",
                         'tmkasun_sample="KasunThennakoon"; Path=/apis; HttpOnly; Domain=localhost')
        self.end_headers()
        request_headers = {}
        for header in self.headers._headers:
            request_headers[header[0]] = header[1]
        response = {
            'description': "This response contains all the information came into the endpoint server including request headers and body",
            'ok': 200,
            'request_connection': {
                'ip': self.client_address[0],
                'port': self.client_address[1]
            },
            'path': self.path,
            'request_headers': request_headers
        }
        jresponse = json.dumps(response)
        self.wfile.write(str.encode(jresponse))

    @staticmethod
    def run():
        port = EndpointHandler.port
        print('INFO: Mock Endpoint Server listening on localhost:{}...'.format(port))
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.TCPServer(('', port), EndpointHandler)
        httpd.serve_forever()

    port = 8000


def main():
    """
        Run as a standalone server if needed
    """
    EndpointHandler.run()


if __name__ == '__main__':
    main()
