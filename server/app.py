#!/usr/bin/env python3
"""JALDORX local job server.

Standard-library-only starter server for the future KAGE X2.
It intentionally does NOT expose the server to the public internet.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import threading
import time
import uuid

HOST = os.environ.get("JALDORX_HOST", "127.0.0.1")
PORT = int(os.environ.get("JALDORX_PORT", "8765"))

jobs = {}
lock = threading.Lock()


def new_job(payload):
    job_id = str(uuid.uuid4())
    job = {
        "id": job_id,
        "status": "queued",
        "product": payload.get("product", ""),
        "idea": payload.get("idea", ""),
        "duration": payload.get("duration", ""),
        "format": payload.get("format", ""),
        "image": payload.get("image"),
        "created_at": int(time.time()),
        "result": None,
    }
    with lock:
        jobs[job_id] = job
    return job


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            return self.send_json(200, {"ok": True, "service": "JALDORX KI-Animator"})
        if self.path == "/jobs":
            with lock:
                data = list(jobs.values())
            return self.send_json(200, {"jobs": data})
        if self.path.startswith("/jobs/"):
            job_id = self.path.split("/")[-1]
            with lock:
                job = jobs.get(job_id)
            if not job:
                return self.send_json(404, {"error": "Job nicht gefunden"})
            return self.send_json(200, job)
        return self.send_json(404, {"error": "Nicht gefunden"})

    def do_POST(self):
        if self.path != "/jobs":
            return self.send_json(404, {"error": "Nicht gefunden"})

        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            return self.send_json(400, {"error": "Ungültiges JSON"})

        if not payload.get("idea"):
            return self.send_json(400, {"error": "idea fehlt"})
        if payload.get("duration") not in ("5", "10"):
            return self.send_json(400, {"error": "duration muss 5 oder 10 sein"})
        if payload.get("format") not in ("9:16", "16:9", "1:1"):
            return self.send_json(400, {"error": "ungültiges Format"})

        job = new_job(payload)
        return self.send_json(202, job)


if __name__ == "__main__":
    print(f"JALDORX Job Server läuft auf http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
