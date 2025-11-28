#!/usr/bin/env python3
"""
Simple HTTP server to view the Twitter Conflict Map Generator dashboard
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow iframe loading
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def main():
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    Handler = MyHTTPRequestHandler

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            url = f"http://localhost:{PORT}/index.html"
            print("=" * 60)
            print("Twitter Conflict Map Generator - Web Server")
            print("=" * 60)
            print(f"\n✓ Server started at: {url}")
            print(f"\n📍 Opening in your browser...")
            print(f"\nPress Ctrl+C to stop the server\n")
            print("=" * 60)

            # Open browser
            webbrowser.open(url)

            # Serve forever
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
        sys.exit(0)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n✗ Error: Port {PORT} is already in use")
            print(f"Try a different port or stop the other server\n")
            sys.exit(1)
        else:
            raise

if __name__ == "__main__":
    main()
