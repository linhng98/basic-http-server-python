'''
    - This server store record pair of shortURL:longURL
    - Redirect website after receive GET request (shortURL in param)
    ex: localhost:8000/abc_xyz (abc_xyz is shortURL stored in record)
'''


from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import parse_qs
from urllib.parse import urlparse
from urllib.parse import unquote
import requests

# dictionary : shortURL/longURL
record = dict()

# default form for input
form = """\
<!DOCTYPE html>

<head>
    <meta charset="utf-8">
    <title>Shorten URL form</title>
</head>

<body>
    <form action="http://localhost:8000/" method="POST">
        <label>Long URL:
            <input type="text" name="longURL">
        </label>
        <br>
        <label>Short URL:
            <input type="text" name="shortURL">
        </label>
        <br>
        <button type="submit">Submit this shit!</button>
    </form>
</body>"""


def checkURL(url, timeout=5):
    # check this url is reachable or not
    try:
        r = requests.get(url, timeout=timeout)
        return r.status_code == 200
    except requests.RequestException:
        return False


class Shortener(BaseHTTPRequestHandler):
    def do_POST(self):
        '''
            To do:
                1. Get length content of body
                2. Get content of param then parse
                3. If shortURL already exist return error
                4. If longURL invalid return error
                4. Store shortURL:longURL pair to record
                5. Respond 303 (redirect to long URL)
        '''
        # Get length of params
        length = int(self.headers.get('Content-Length'))
        body = self.rfile.read(length).decode()

        # Parse params from body content
        params = parse_qs(unquote(body))
        shortURL = params['shortURL'][0]
        longURL = params['longURL'][0]

        # if collision (have 2 same key in record)
        if shortURL in list(record.keys()):
            error_message = "This shortURL '{}' " + \
                "already in record, please choose another"
            self.response_back(error_message.format(shortURL), 404)
        else:
            # check this longURL is reachable or not
            if checkURL(longURL) is False:
                error_message = "This longURL '{}' is invalid URL, " + \
                    "please choose another"
                self.response_back(error_message.format(shortURL), 404)
            else:
                record[shortURL] = longURL
                self.response_back('', 303, longURL)

    def do_GET(self):
        '''
            To do:
                1. Parse param then get path
                2. If path is empty, response form
                3. Else search path in record keys, if path not exist
                   return error invalid shortURL
        '''
        shortURL = unquote(urlparse(self.path).path[1:])

        # localhost:8000/
        if not shortURL:
            self.response_back()
        else:
            if shortURL in list(record.keys()):
                self.response_back('', 303, record[shortURL])
            else:
                error_message = "This shortURL '{}' is not bookmarked"
                self.response_back(error_message.format(shortURL), 404)

    def response_back(self, message=form, code=200, location=''):
        if code == 303:
            self.send_response(303)
            self.send_header('Location', location)
            self.end_headers()
        else:
            self.send_response(code)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(message.encode())


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, Shortener)
    httpd.serve_forever()
