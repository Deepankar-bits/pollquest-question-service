import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BACKEND_URL = "http://localhost:8008/pollquest-service/api/v1"


class RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Disable default logging to stderr
        pass

    def do_GET(self):
        parsed_path = urlparse(self.path)
        question_id = parsed_path.path.split('/')[-1]
        logger.info(f"Received GET request for question ID: {question_id}")

        response = requests.get(f"{BACKEND_URL}/questions?id={question_id}")

        if response.status_code == 200:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            logger.debug("Response received")
            self.wfile.write(response.content)
        else:
            self.send_error(response.status_code)

    def do_POST(self):
        parsed_path = self.path.split('/')
        path_name = parsed_path[-1]

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        logger.info(f"Received POST request for path: {path_name}")

        if path_name == 'addQuestion':
            question_id = data.get('questionId')
            question = data.get('question')

            if not question_id or not question:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing questionId or question"}).encode())
                return

            response = requests.post(f"{BACKEND_URL}/addQuestion", json={"questionId": question_id, "question": question})

            if response.status_code == 200:
                get_response = requests.get(f"{BACKEND_URL}/questions?id={question_id}")

                if get_response.status_code == 200:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    logger.info("Response received from backend service:")
                    logger.info(get_response.json())  # Log the response
                    self.wfile.write(get_response.content)
                else:
                    self.send_error(get_response.status_code)
            else:
                self.send_error(response.status_code)

        elif path_name == 'generateCode':
            description = data.get('description')

            if not description:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing description"}).encode())
                return

            response = requests.post(f"{BACKEND_URL}/generateCode", json={"description": description})

            if response.status_code == 200:
                self.send_response(200)
                self.send_header('Content-type', 'application/text')
                self.end_headers()
                logger.info("Response received from backend service:")
                logger.info(response.text)
                self.wfile.write(response.content)
            else:
                self.send_error(response.status_code)


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080, service_name="pollquest-question-service"):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logger.info(f"Server running on http://localhost:{port}/{service_name}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
