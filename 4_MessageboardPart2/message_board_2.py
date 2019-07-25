'''
    This HTTP server serve both GET and POST request
        - Respond form when receive GET request
        - Respond message when receive POST request
'''

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs


form = '''<!DOCTYPE html>

<head>
    <meta charset="utf-8">
    <title>Basic Login Form</title>
</head>

<body>
    <form action="http://localhost:8000/" method="POST">
        <label>Magic input:
            <input type="text" name="message">
        </label>
        <br>
        <button type="submit">Post it!</button>
    </form>
</body>
'''


class MessageboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        '''
            To do :
                1. Send response code
                2. Send headers
                3. Write body content
        '''

        self.send_response(200)
        self.send_header('content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(form.encode())

    def do_POST(self):
        '''
            To do:
                1. Get length of messgae
                2. Read the correct amount of data from request (POST)
                3. Extract message from data
                4. Send back data to client
        '''

        # get data from request
        length = int(self.headers.get('content-length', 0))
        data = self.rfile.read(length).decode()
        message = parse_qs(data)['message'][0]

        # send respond
        self.send_response(200)
        self.send_header('content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode())


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MessageboardHandler)
    httpd.serve_forever()
