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

    def common_handler(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        request_headers = {}
        for header in self.headers._headers:
            request_headers[header[0]] = header[1]
        response = {
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
