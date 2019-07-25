'''
    This server is a HTTP that receive request from client and respond
    with a friendly greeting. Run this program on terminal and access
    the server at localhost port 8000
'''

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler


class EchoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        '''
            To do :
                1. Send response code
                2. Send headers
                3. Write body content
        '''

        self.send_response(200)

        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        # Parse query content
        self.wfile.write(self.path[1:].encode())


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, EchoHandler)
    httpd.serve_forever()
