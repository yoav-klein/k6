
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler

def main():
    server = HTTPServer(('', 80), SimpleHTTPRequestHandler)

    server.serve_forever()


if __name__ == "__main__":
    main()
