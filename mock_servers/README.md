# Mock Endpoint Server
=========================

## Description
---------------

This is a mock endpoint server written in Python, designed for testing and mocking HTTP requests. It includes features such as streaming APIs, digest authentication, JWT decoding, and more.

## Features
--------

* Streaming APIs
* Digest authentication
* JWT decoding
* Support for various HTTP methods (GET, POST, PUT, DELETE, etc.)
* Cache control headers
* Access control headers (CORS)
* Support for serving media files (PDF, JPEG, PNG, etc.)

## Usage
-----

To run the server, simply execute the Python script. By default, it will listen on port 8080. You can test the server using a tool like `curl` or a web browser.

## Endpoints
----------

* `/stream`: Streaming API endpoint
* `/digestme`: Digest authentication test endpoint

## Query Parameters
------------------

* `sleep`: Simulates a delay in the server response time (in milliseconds)
* `kdelay`: Simulates a delay in the server processing time (in milliseconds)

## Headers
---------

* `Authorization`: Digest authentication header
* `X-JWT-Assertion`: JWT decoding header

## Dependencies
------------

* `python_digest`
* `jwt`
* `dicttoxml`

## License
-------

This software is licensed under the MIT License.

## Author
------

Kasun Thennakoon

## Acknowledgments
----------------

This software uses the following third-party libraries:

* `python_digest`
* `jwt`
* `dicttoxml`