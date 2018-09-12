#!/usr/bin/env python3
import json
import base64
import time
try:
    import python_digest
except ImportError:
    print("WARN: Can't find python_digest module , Hence you won't able to use Digest Auth feature")
from http import server, HTTPStatus
import socketserver
import ssl
from os import path


class EndpointHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.common_handler()

    def do_POST(self):
        self.common_handler()

    def do_DELETE(self):
        self.common_handler()

    def do_PATCH(self):
        self.common_handler()

    def do_HEAD(self):
        self.common_handler()

    def do_PUT(self):
        self.common_handler()

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.OK)
        requested_headers = self.headers.get("Access-Control-Request-Headers")
        requested_methods = self.headers.get("Access-Control-Request-Method")
        requested_origin = self.headers.get("Origin")
        print("*** CORS Info: requested_origin = {}\n requested_methods = {}\n requested_headers = {}".format(
            requested_origin, requested_methods, requested_headers))
        self.send_header("Access-Control-Allow-Origin", requested_origin)
        # Pseudo code
        # If requested_origin in allowed origin(s) or in configuration:
        #   Add domain to Access-Control-Allow-Origin response header
        self.send_header("Access-Control-Allow-Headers", requested_headers)
        self.send_header("Access-Control-Allow-Methods", requested_methods)
        self.send_header("Access-Control-Max-Age", 86400)
        # Pseudo code
        # If requested_headers in safelisted-request-headers #https://fetch.spec.whatwg.org/#cors-safelisted-request-header
        # Append header to Access-Control-Allow-Headers header value
        self.end_headers()
        request_headers = {}
        for header in self.headers._headers:
            request_headers[header[0]] = header[1]
        print(request_headers)
        self.wfile.write(b"")

    """
      - 1xx: Informational - Request received, continuing process
      - 2xx: Success - The action was successfully received,
        understood, and accepted
      - 3xx: Redirection - Further action must be taken in order to
        complete the request
      - 4xx: Client Error - The request contains bad syntax or cannot
        be fulfilled
      - 5xx: Server Error - The server failed to fulfill an apparently
        valid request
    """

    def setStatusCode(self):
        # self.send_response(HTTPStatus.FORBIDDEN)
        self.send_response(HTTPStatus.OK)
        # self.send_response(HTTPStatus.OK)

    def common_handler(self):
        self.setStatusCode()
        # print(self.path)
        auth_params = self.decodeAuthHeader()
        """
            Handle digest auth request if the request path contains the text `digestme`
            According to the Digest Auth protocol , In the initial request to the secured page, Server will respond with the WWW-Authenticate header
            and in the consequent call,client auth will be handle with previously issued digest.
            Ref: http://qnimate.com/understanding-http-authentication-in-depth/
        """
        if 'digestme' in self.path.lower() and auth_params is None:
            print("Potential Digest auth request received!")
            digest_header = self.getDigestAuth()
            print("Adding header WWW-Authenticate : {}".format(digest_header))
            self.send_header("WWW-Authenticate", digest_header)
        self.send_header("Content-type", "application/json")
        requested_origin = self.headers.get("Origin")
        self.send_header("Access-Control-Allow-Origin", requested_origin)
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Set-Cookie",
                         'tmkasun_sample="KasunThennakoon"; Path=/apis; HttpOnly; Domain=localhost')
        self.end_headers()
        request_headers = {}
        request_body = self.getBody()
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
            'HTTP Method': self.command,
            'request_headers': request_headers,
            'body': request_body,
            'auth': auth_params
        }
        jresponse = json.dumps(response)
        # print(response)
        self.wfile.write(str.encode(jresponse))

    @staticmethod
    def run():
        port = EndpointHandler.port
        print('INFO: (Secured: {})Mock Endpoint Server listening on localhost:{}...'.format(EndpointHandler.secured,
                                                                                            port))
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.TCPServer(('', port), EndpointHandler)
        cert_path = path.dirname(__file__)+'yourpemfile.pem'
        print("DEBUG: cert_path = " + cert_path)
        if EndpointHandler.secured:
            httpd.socket = ssl.wrap_socket(
                httpd.socket, server_side=True, certfile=cert_path)
        httpd.serve_forever()

    """
            while True:
                line = self.rfile.readline().decode("UTF-8").strip()
                if(len(line) == 0):
                    break
                request_body += line
    """

    def getBody(self):
        blocking = False
        content_length = int(self.headers.get("content-length", -1))
        content_type = self.headers.get("content-type", -1)
        method = self.command
        if blocking and content_length == -1 and method in ["POST", "PUT", "PATCH"] and content_type != -1:
            # Just giving a try here, The `content-length` header could be missing in case of HTTP1.1 chunked transfer encoding state
            # So giving it a try, If there is no data while satisfying the above condition , the rfile.readline() will hang!!!
            request_body = ""
            while True:
                line = self.rfile.readline().decode("UTF-8").strip()
                if(len(line) == 0):
                    break
                request_body += line
            return request_body
        return None if content_length in [0, -1] else self.rfile.read(content_length).decode("UTF-8")

    def getDigestAuth(self):
        www_authenticate_header = python_digest.build_digest_challenge(
            time.time(), self.digestAuthSecret, 'API', 'opaque_ASVASASFAS2131', False)
        return www_authenticate_header

    def decodeAuthHeader(self):
        auth_header = self.headers.get("Authorization", -1)
        if auth_header == -1:
            return None
        auth_props = auth_header.split(' ')
        auth_type = auth_props[0]
        if auth_type.lower() == 'basic':
            auth_params = base64.b64decode(
                auth_header.split(' ')[-1]).decode('UTF-8').split(':')
            return {'username': auth_params[0], 'password': auth_params[1]}
        else:
            return auth_header

    port = 8000
    secured = False
    digestAuthSecret = 'this()is+my#s3cR3a1i4'


def main():
    """
        Run as a standalone server if needed
    """
    EndpointHandler.run()


if __name__ == '__main__':
    main()
