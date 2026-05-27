kimport json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

# Configure logging
logging.basicConfig(level=logging.INFO)

# Mock Database
TASKS_DB = [
    {"id": 1, "title": "Setup local target server", "status": "Completed"},
    {"id": 2, "title": "Configure Jenkins CI/CD pipeline", "status": "In Progress"},
    {"id": 3, "title": "Expose web service via Docker", "status": "Pending"}
]


class ProductionAppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Health-check endpoint for monitoring/uptime tools
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"status": "UP", "database": "CONNECTED"}
            self.wfile.write(json.dumps(response).encode())
            logging.info("Health check endpoint hit - 200 OK")

        # Main API endpoint fetching backend data
        elif self.path == '/api/tasks':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            # Cross-Origin Resource Sharing header
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(TASKS_DB).encode())
            logging.info("Tasks API data requested - 200 OK")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Resource Not Found")
            logging.warning(f"404 Resource Not Found requested: {self.path}")


if __name__ == "__main__":
    server_address = ('0.0.0.0', 5000)
    httpd = HTTPServer(server_address, ProductionAppHandler)
    logging.info("Production Microservice starting on container port 5000...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Server shutting down cleanly...")
