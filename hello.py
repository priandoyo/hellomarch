from http.server import HTTPServer, BaseHTTPRequestHandler

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(b"""
        <html>
            <body>
                <h1>Hello World!</h1>
                <p>This is a Python web server.</p>
            </body>
        </html>
        """)

server = HTTPServer(("0.0.0.0", 8080), HelloHandler)

print("Server running on port 8080...")
server.serve_forever()
