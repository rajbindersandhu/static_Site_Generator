import os
import argparse # This module is used to parse CLI arguments
from http.server import HTTPServer, SimpleHTTPRequestHandler

# This class will handel CORS(Cross-origin resource sharing) requests 
class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # This allows all the requests from any domain
        self.send_header("Access-Control-Allow-Origin",  "*")
        # This allow only GET and OPTION request to the server for CORS
        # OPTIONS is a request send to server before any CORS request to know what the server allows for CORS
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Accees-Contrl-Allow-Headers", "*")
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.end_headers()

def run(server_class=HTTPServer, handler_class=CORSHTTPRequestHandler, port=8000, directory=None):
    if directory: # Change the current working directory if directory is specified
        os.chdir(directory)
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving HTTP on http://localhost:{port} from directory '{directory}'...")
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP Server with CORS")
    # this helps to create an optional flag to capture directory name
    parser.add_argument("--dir", type=str, help="Directory to serve files from", default=".") # defaukt is current directory
    parser.add_argument("--port", type=int, help="Port to serve HTTP on", default=8888)
    args = parser.parse_args()

    run(port=args.port, directory=args.dir)

