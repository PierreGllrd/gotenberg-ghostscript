#!/usr/bin/env python3
"""
Serveur HTTP simple pour post-traiter les PDFs avec Ghostscript
Écoute sur le port 3001 et post-traite les PDFs envoyés via POST
"""

import os
import sys
import subprocess
import tempfile
from http.server import HTTPServer, BaseHTTPRequestHandler

class PDFA3Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/fix-pdfa3':
            self.send_error(404)
            return
        
        content_length = int(self.headers.get('Content-Length', 0))
        pdf_data = self.rfile.read(content_length)
        
        if len(pdf_data) == 0:
            self.send_error(400, "No PDF data received")
            return
        
        # Créer des fichiers temporaires
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as input_file:
            input_file.write(pdf_data)
            input_path = input_file.name
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as output_file:
            output_path = output_file.name
        
        try:
            # Post-traiter avec Ghostscript
            result = subprocess.run([
                'gs', '-dPDFA=3', '-dBATCH', '-dNOPAUSE', '-dNOOUTERSAVE',
                '-sColorConversionStrategy=RGB',
                '-sOutputFile=' + output_path,
                '-sDEVICE=pdfwrite',
                '-dPDFACompatibilityPolicy=1',
                '-dUseCIEColor=true',
                input_path
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output_path):
                # Lire le PDF corrigé
                with open(output_path, 'rb') as f:
                    corrected_pdf = f.read()
                
                # Envoyer le PDF corrigé
                self.send_response(200)
                self.send_header('Content-Type', 'application/pdf')
                self.send_header('Content-Length', str(len(corrected_pdf)))
                self.end_headers()
                self.wfile.write(corrected_pdf)
            else:
                self.send_error(500, f"Ghostscript failed: {result.stderr}")
        except Exception as e:
            self.send_error(500, str(e))
        finally:
            # Nettoyer les fichiers temporaires
            try:
                os.unlink(input_path)
                if os.path.exists(output_path):
                    os.unlink(output_path)
            except:
                pass
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        # Ne pas logger pour éviter le spam
        pass

if __name__ == '__main__':
    port = int(os.environ.get('POST_PROCESS_PORT', 3001))
    server = HTTPServer(('0.0.0.0', port), PDFA3Handler)
    print(f'PDF/A-3 post-process server listening on port {port}')
    server.serve_forever()

