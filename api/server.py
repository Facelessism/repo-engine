import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from engine.repository import RepositoryEngine


engine = RepositoryEngine()


class RequestHandler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data).encode()

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self.send_json({
                "message": "Repo Engine API"
            })
            return

        self.send_json({
            "error": "Not found"
        }, 404)

    def do_POST(self):
        if self.path != "/api/tree":
            self.send_json({
                "error": "Not found"
            }, 404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))

            if not length:
                raise ValueError("Request body is required.")

            body = self.rfile.read(length)
            data = json.loads(body)

            url = data.get("url")

            if not isinstance(url, str) or not url.strip():
                raise ValueError("GitHub repository URL is required.")

            result = engine.generate(url.strip())
            self.send_json(result)

        except json.JSONDecodeError:
            self.send_json({
                "error": "Invalid JSON body."
            }, 400)

        except Exception as error:
            self.send_json({
                "error": str(error)
            }, 400)


def main():
    server = HTTPServer(
        ("127.0.0.1", 8000),
        RequestHandler
    )

    print("Repo Engine API running on http://127.0.0.1:8000")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
