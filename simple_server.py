#!/usr/bin/env python3
"""
Einfacher HTTP Server für Testing
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/templates/index.html'
        return super().do_GET()
    
    def end_headers(self):
        # CORS Headers hinzufügen
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def run_server(port=8000):
    """Starte den einfachen HTTP Server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomHandler)
    print(f"🚀 Server läuft auf http://localhost:{port}")
    print("Drücken Sie Ctrl+C zum Beenden")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server gestoppt")
        httpd.shutdown()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
