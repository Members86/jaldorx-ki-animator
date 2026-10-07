#!/usr/bin/env python3
"""JALDORX local job server for the future KAGE X2."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json, os, threading, time, uuid

HOST = os.environ.get("JALDORX_HOST", "127.0.0.1")
PORT = int(os.environ.get("JALDORX_PORT", "8765"))
jobs, lock = {}, threading.Lock()

def new_job(payload):
    job = {
        "id": str(uuid.uuid4()), "status": "queued",
        "product": payload.get("product", ""), "idea": payload.get("idea", ""),
        "duration": payload.get("duration", ""), "format": payload.get("format", ""),
        "image": payload.get("image"), "created_at": int(time.time()), "result": None
    }
    with lock: jobs[job["id"]] = job
    return job

class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        return self.send_json(204, {})

    def do_GET(self):
        if self.path == "/health":
            return self.send_json(200, {"ok": True, "service": "JALDORX KI-Animator", "version": 1})
        if self.path == "/jobs":
            with lock: data = list(jobs.values())
            return self.send_json(200, {"jobs": data})
        if self.path.startswith("/jobs/"):
            with lock: job = jobs.get(self.path.split("/")[-1])
            return self.send_json(200, job) if job else self.send_json(404, {"error": "Job nicht gefunden"})
        return self.send_json(404, {"error": "Nicht gefunden"})

    def do_POST(self):
        if self.path != "/jobs":
            return self.send_json(404, {"error": "Nicht gefunden"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode())
        except Exception:
            return self.send_json(400, {"error": "Ungültiges JSON"})
        if not payload.get("idea"):
            return self.send_json(400, {"error": "idea fehlt"})
        if str(payload.get("duration")) not in ("5", "10"):
            return self.send_json(400, {"error": "duration muss 5 oder 10 sein"})
        if payload.get("format") not in ("9:16", "16:9", "1:1"):
            return self.send_json(400, {"error": "ungültiges Format"})
        return self.send_json(202, new_job(payload))

if __name__ == "__main__":
    print(f"JALDORX Job Server läuft auf http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
