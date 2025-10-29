import requests
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsedPath = urlparse(self.path)
        params = parse_qs(parsedPath.query)
        if 'code' in params:
            self.server.authorizationCode = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Authorization successful!</h1><p>You can close this window.</p></body></html>")
            threading.Thread(target=self.server.shutdown).start()
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Error</h1><p>Authorization code not found.</p></body></html>")

def buildAuthorizationURL(clientID: str, redirectURI: str, scopes: list[str]) -> str:
    scope_str = ' '.join(scopes)
    return (
        f"https://id.twitch.tv/oauth2/authorize"
        f"?client_id={clientID}"
        f"&redirect_uri={redirectURI}"
        f"&response_type=code"
        f"&scope={scope_str}"
    )

def startLocalServer(port: int = 8765):
    server_address = ('', port)
    httpd = HTTPServer(server_address, OAuthHandler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    return httpd

def getToken(clientID: str, clientSecret: str, code: str, redirectURI: str) -> dict:
    url = 'https://id.twitch.tv/oauth2/token'
    data={
        'client_id': clientID,
        'client_secret': clientSecret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirectURI
    }
    res = requests.post(url, data=data)
    res.raise_for_status()
    return res.json()