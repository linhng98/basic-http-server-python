from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

list_message = []

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
<pre>
{}
</pre>
</body>
'''


class MessageboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        '''
            To do :
                1. Send response 200 success code
                2. Send headers
                3. Write body content include list message
        '''

        self.send_response(200)
        self.send_header('content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write((form.format('\n'.join(list_message))).encode())

    def do_POST(self):
        '''
            To do:
                1. Get length of messgae
                2. Read the correct amount of data from request (POST)
                3. Extract message from data then append to list message
                4. Send status code 302
        '''

        # get data from request then append
        length = int(self.headers.get('content-length', 0))
        data = self.rfile.read(length).decode()
        message = parse_qs(data)['message'][0]
        list_message.append(message)

        # send respond
        self.send_response(303)  # redirect via GET
        self.send_header('Location', '/')
        self.end_headers()


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MessageboardHandler)
    httpd.serve_forever()
