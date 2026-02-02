from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import threading
import time
import uuid
import sys

class CSVAPIHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/api/v1/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "UP",
                "service": "csv-processing-api",
                "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
                "version": "1.0.0",
                "components": {
                    "java": "simulated",
                    "spring-boot": "simulated",
                    "python-worker": "ready"
                }
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path.startswith('/api/v1/csv/status/'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            process_id = self.path.split('/')[-1]
            response = {
                "status": "success",
                "message": "Check logs for details",
                "processId": process_id
            }
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/v1/csv/process':
            process_id = str(uuid.uuid4())[:8]
            
            # Executa o Python worker em uma thread separada
            def run_worker():
                try:
                    print(f"\n[INFO] Iniciando processamento CSV (ID: {process_id})")
                    result = subprocess.run(
                        ['python', '../python-worker/worker.py', process_id],
                        capture_output=True,
                        text=True,
                        encoding='utf-8'
                    )
                    print(f"[SUCCESS] Processamento concluido (ID: {process_id})")
                    if result.stdout:
                        print(f"Output: {result.stdout}")
                    if result.stderr:
                        print(f"Errors: {result.stderr}")
                except Exception as e:
                    print(f"[ERROR] Erro no worker: {e}")
            
            thread = threading.Thread(target=run_worker)
            thread.daemon = True
            thread.start()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "success",
                "message": "Processing started",
                "processId": process_id,
                "note": "Java API simulated - Python worker running"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[API] {args[0]} {args[1]} - {args[2]}")

def main():
    """Start the API server"""
    print("=" * 60)
    print("CSV Corporate Pipeline - API Simulator")
    print("=" * 60)
    print("Esta API simula o comportamento do Spring Boot em Python")
    print("O Python Worker é REAL e processa CSVs de verdade")
    print("")
    print("Endpoints disponiveis:")
    print("  GET  http://localhost:8080/api/v1/health")
    print("  POST http://localhost:8080/api/v1/csv/process")
    print("")
    print("Python Worker:")
    print("  O worker em python-worker/ é executado quando você faz POST")
    print("  O resultado é salvo em python-worker/data/output.csv")
    print("")
    print("Iniciando servidor na porta 8080...")
    print("=" * 60)
    
    # Configura encoding para Windows
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    server = HTTPServer(('localhost', 8080), CSVAPIHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Servidor encerrado")
        server.server_close()

if __name__ == '__main__':
    main()