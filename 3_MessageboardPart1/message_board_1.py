'''
    This server receive POST request and return message
'''

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs


class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        '''
            To do:
                - Get length of messgae
                - Read the correct amount of data from request (POST)
                - Extract message field from data
                - Send back data to client
        '''

        # get data from request
        length = int(self.headers.get('content-length', 0))
        data = self.rfile.read(length).decode()
        message = parse_qs(data)['message'][0]

        # send respond
        self.send_response(200)

        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        self.wfile.write(message.encode())


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MessageHandler)
    httpd.serve_forever()
