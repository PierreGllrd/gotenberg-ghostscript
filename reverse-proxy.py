#!/usr/bin/env python3
"""
Reverse proxy HTTP qui route les requêtes :
- /fix-pdfa3 -> Serveur de post-traitement (port 3001)
- Tout le reste -> Gotenberg (port 3000)
"""

import os
import sys
import http.server
import socketserver
import urllib.request
import urllib.parse

# Configuration
GOTENBERG_HOST = 'localhost'
GOTENBERG_PORT = 3000
POST_PROCESS_HOST = 'localhost'
POST_PROCESS_PORT = 3001
PROXY_PORT = int(os.environ.get('PORT', 3000))

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        # Gérer HEAD pour les health checks
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        self.proxy_request('GET')
    
    def do_POST(self):
        self.proxy_request('POST')
    
    def do_PUT(self):
        self.proxy_request('PUT')
    
    def do_DELETE(self):
        self.proxy_request('DELETE')
    
    def proxy_request(self, method):
        # Décider où router la requête
        if '/fix-pdfa3' in self.path:
            target_host = POST_PROCESS_HOST
            target_port = POST_PROCESS_PORT
        else:
            target_host = GOTENBERG_HOST
            target_port = GOTENBERG_PORT
        
        # Lire le corps de la requête
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b''
        
        # Construire l'URL cible
        target_url = f'http://{target_host}:{target_port}{self.path}'
        if self.query_string:
            target_url += '?' + self.query_string
        
        try:
            # Créer la requête
            req = urllib.request.Request(target_url, data=body, method=method)
            
            # Copier les headers (sauf Host)
            for header, value in self.headers.items():
                if header.lower() != 'host' and header.lower() != 'connection':
                    req.add_header(header, value)
            
            # Envoyer la requête
            with urllib.request.urlopen(req, timeout=60) as response:
                # Copier les headers de la réponse
                self.send_response(response.getcode())
                for header, value in response.headers.items():
                    if header.lower() not in ['connection', 'transfer-encoding']:
                        self.send_header(header, value)
                self.end_headers()
                
                # Copier le corps de la réponse
                self.wfile.write(response.read())
                
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            print(f"Error proxying request: {e}", file=sys.stderr, flush=True)
            self.send_error(502, f"Proxy error: {str(e)}")
    
    def log_message(self, format, *args):
        # Log simplifié
        if '/fix-pdfa3' in self.path or self.path == '/':
            print(f"{self.address_string()} - {format % args}", flush=True)

def main():
    handler = ProxyHandler
    httpd = socketserver.TCPServer(("0.0.0.0", PROXY_PORT), handler)
    
    print(f'Reverse proxy listening on port {PROXY_PORT}', flush=True)
    print(f'Routing /fix-pdfa3 -> {POST_PROCESS_HOST}:{POST_PROCESS_PORT}', flush=True)
    print(f'Routing everything else -> {GOTENBERG_HOST}:{GOTENBERG_PORT}', flush=True)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...", flush=True)
        httpd.shutdown()

if __name__ == '__main__':
    main()
