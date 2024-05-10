from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from urllib.parse import urlparse, parse_qs
BACKEND_URL = "http://localhost:8008/pollquest-service/api/v1"

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        question_id = parsed_path.path.split('/')[-1]
        print(question_id, flush = True) 
        #print(endl)
        response = requests.get(f"{BACKEND_URL}/questions?id={question_id}")
        #response = requests.get(f"{BACKEND_URL}")

        self.send_response(response.status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(json.dumps(response.json()).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        data = json.loads(post_data.decode('utf-8'))

        description = data.get('description', None)
        if description is None:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Description field missing"}).encode())
            return

        response = requests.post(f"{BACKEND_URL}/post", json={"description": description})

        self.send_response(response.status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(json.dumps({"message": "Data posted successfully"}).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    print("hello one", flush = True) 
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}", flush = True)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
