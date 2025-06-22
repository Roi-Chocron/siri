import http.server
import socketserver
import json
import subprocess
import os

PORT = 8001  # שרת API

class ApiHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # הדפסה מפורטת של כל בקשה
        print("[API LOG]", self.address_string(), '-', format % args)

    def do_OPTIONS(self):
        print("[DEBUG] קיבלתי בקשת OPTIONS מ-", self.client_address)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.end_headers()

    def do_POST(self):
        print(f"[DEBUG] קיבלתי POST ל-{self.path} מ-{self.client_address}")
        if self.path == "/send":
            self.handle_gemini()
        else:
            print(f"[ERROR] נתיב לא קיים: {self.path}")
            self.send_error(404, "Not found")

    def handle_gemini(self):
        content_length = int(self.headers.get('Content-Length', 0))
        print(f"[DEBUG] Content-Length: {content_length}")
        body = self.rfile.read(content_length)
        print(f"[DEBUG] Body: {body}")
        try:
            data = json.loads(body)
            user_text = data.get("text", "")
            print(f"[DEBUG] user_text: {user_text}")
            result = subprocess.run([
                "python", "gemini_basic.py", user_text
            ], capture_output=True, text=True)
            print(f"[DEBUG] Subprocess returncode: {result.returncode}")
            print(f"[DEBUG] Subprocess stdout: {result.stdout}")
            print(f"[DEBUG] Subprocess stderr: {result.stderr}")
            if result.returncode == 0:
                answer = result.stdout.strip()
                response = {"type": "system", "text": answer}
            else:
                response = {"type": "system", "text": f"שגיאה בהרצת Gemini: {result.stderr}"}
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            import traceback
            print("[ERROR] Exception occurred:")
            traceback.print_exc()
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"type": "system", "text": f"שגיאה בשרת: {str(e)}"}, ensure_ascii=False).encode('utf-8'))

if __name__ == "__main__":
    print(f"API server running at http://localhost:{PORT}/send")
    with socketserver.TCPServer(("", PORT), ApiHandler) as httpd:
        httpd.serve_forever()
