from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
from os import environ, path
from threading import Thread
import signal
from pg8000.native import Connection

logger = logging.getLogger('app')

HTTP_HOST = environ.get('HTTP_HOST', '0.0.0.0')
HTTP_PORT = environ.get('HTTP_PORT', 8000)
PG_USER = environ.get('PG_USER', 'postgres')
PG_PASS = environ.get('PG_PASSWORD')
PG_DB = environ.get('PG_DB', 'postgres')
PG_HOST = environ.get('PG_HOST')
PG_PORT = environ.get('PG_PORT', '5432')

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/check-connection':
            try:
                with Connection(PG_USER,
                                password=PG_PASS,
                                host=PG_HOST,
                                port=PG_PORT,
                                database=PG_DB) as conn:
                    conn.run("SELECT 1")
                self.send_response(200)
                self.end_headers()
            except Exception:
                logger.exception("Failed to connect to Postgres.")
                self.send_response(503)
                self.end_headers()
        elif self.path == '/':
            filepath = path.join('index.html')
            with open(filepath, 'rb') as file:
                content = file.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger.info(f'Serving on {HTTP_HOST}:{HTTP_PORT}')
    server = HTTPServer((HTTP_HOST, HTTP_PORT), Handler)
    signal.signal(signal.SIGTERM, lambda _s, _f: server.shutdown())
    server_thread = Thread(target=server.serve_forever)
    server_thread.start()
    server_thread.join()
