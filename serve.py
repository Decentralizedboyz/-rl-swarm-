from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    # Change to the frontend directory
    os.chdir("frontend")
    
    # Start the server
    port = 8080
    print(f"Starting server on port {port}...")
    httpd = HTTPServer(("", port), CORSRequestHandler)
    print(f"Server running at http://localhost:{port}")
    httpd.serve_forever() 