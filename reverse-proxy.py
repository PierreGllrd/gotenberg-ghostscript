#!/usr/bin/env python3
"""
Reverse proxy HTTP qui route les requêtes :
- /fix-pdfa3 -> Serveur de post-traitement (port 3001)
- Tout le reste -> Gotenberg (port 3000)
"""

import os
import sys
import socket
import threading
from urllib.parse import urlparse

# Configuration
GOTENBERG_HOST = 'localhost'
GOTENBERG_PORT = 3000
POST_PROCESS_HOST = 'localhost'
POST_PROCESS_PORT = 3001
PROXY_PORT = int(os.environ.get('PORT', 3000))

# Si le port est le même que Gotenberg, on change le port interne de Gotenberg
if PROXY_PORT == GOTENBERG_PORT:
    # Le reverse proxy écoute sur le port principal, Gotenberg doit écouter ailleurs
    # Mais en fait, on garde Gotenberg sur 3000 et le proxy écoute sur PORT
    pass

def forward_request(data, target_host, target_port):
    """Forward une requête HTTP vers un service cible"""
    try:
        target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_sock.connect((target_host, target_port))
        target_sock.sendall(data)
        
        response = b''
        while True:
            chunk = target_sock.recv(4096)
            if not chunk:
                break
            response += chunk
        
        target_sock.close()
        return response
    except Exception as e:
        print(f"Error forwarding request: {e}", file=sys.stderr)
        return None

def handle_connection(client_sock, addr):
    """Gère une connexion client"""
    try:
        # Lire la requête
        data = client_sock.recv(8192)
        if not data:
            return
        
        request_str = data.decode('utf-8', errors='ignore')
        first_line = request_str.split('\n')[0] if '\n' in request_str else request_str
        
        # Décider où router
        if '/fix-pdfa3' in first_line:
            target_host = POST_PROCESS_HOST
            target_port = POST_PROCESS_PORT
        else:
            target_host = GOTENBERG_HOST
            target_port = GOTENBERG_PORT
        
        # Forwarder la requête
        response = forward_request(data, target_host, target_port)
        
        if response:
            client_sock.sendall(response)
        else:
            # Erreur 502 Bad Gateway
            error_response = b'HTTP/1.1 502 Bad Gateway\r\n\r\n'
            client_sock.sendall(error_response)
    except Exception as e:
        print(f"Error in handle_connection: {e}", file=sys.stderr)
    finally:
        client_sock.close()

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('0.0.0.0', PROXY_PORT))
    server_sock.listen(100)
    
    print(f'Reverse proxy listening on port {PROXY_PORT}')
    print(f'Routing /fix-pdfa3 -> {POST_PROCESS_HOST}:{POST_PROCESS_PORT}')
    print(f'Routing everything else -> {GOTENBERG_HOST}:{GOTENBERG_PORT}', flush=True)
    
    while True:
        try:
            client_sock, addr = server_sock.accept()
            thread = threading.Thread(target=handle_connection, args=(client_sock, addr))
            thread.daemon = True
            thread.start()
        except KeyboardInterrupt:
            break
    
    server_sock.close()

if __name__ == '__main__':
    main()
