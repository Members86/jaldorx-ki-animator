#!/usr/bin/env python3
"""JALDORX local job server and worker pipeline."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json, os, threading, time, uuid
from pathlib import Path
from urllib.parse import urlparse
from engine import VideoEngine

HOST = os.environ.get("JALDORX_HOST", "127.0.0.1")
PORT = int(os.environ.get("JALDORX_PORT", "8765"))
OUTPUT_DIR = Path(os.environ.get("JALDORX_OUTPUT_DIR", "output"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

jobs, lock = {}, threading.Lock()
engine = VideoEngine()

def new_job(payload):
    job_id = str(uuid.uuid4())
    job = {
        "id": job_id, "status": "queued",
        "product": payload.get("product", ""), "idea": payload.get("idea", ""),
        "duration": str(payload.get("duration", "")), "format": payload.get("format", ""),
        "image": payload.get("image"), "created_at": int(time.time()),
        "result": None, "download_url": None, "error": None
    }
    with lock:
        jobs[job_id] = job
    threading.Thread(target=process_job, args=(job_id,), daemon=True).start()
    return job

def process_job(job_id):
    with lock:
        job = jobs.get(job_id)
        if not job:
            return
        job["status"] = "processing"
    try:
        output_path = OUTPUT_DIR / f"{job_id}.mp4"
        result = engine.generate(
            prompt=job["idea"], duration=int(job["duration"]),
            aspect_ratio=job["format"], image_path=job.get("image"),
            output_path=str(output_path),
        )
        with lock:
            job["status"] = "completed"
            job["result"] = result
            job["download_url"] = f"/results/{job_id}"
    except NotImplementedError as exc:
        with lock:
            job["status"] = "waiting_for_engine"
            job["error"] = str(exc)
    except Exception as exc:
        with lock:
            job["status"] = "failed"
            job["error"] = str(exc)

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
        self.send_json(204, {})

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            return self.send_json(200, {
                "ok": True, "service": "JALDORX KI-Animator",
                "version": 3, "engine": engine.name,
            })
        if path == "/engine":
            return self.send_json(200, engine.status())
        if path == "/jobs":
            with lock:
                data = list(jobs.values())
            return self.send_json(200, {"jobs": data})
        if path.startswith("/jobs/"):
            job_id = path.split("/")[-1]
            with lock:
                job = jobs.get(job_id)
            return self.send_json(200, job) if job else self.send_json(404, {"error": "Job nicht gefunden"})
        if path.startswith("/results/"):
            job_id = path.split("/")[-1]
            file_path = OUTPUT_DIR / f"{job_id}.mp4"
            if not file_path.is_file():
                return self.send_json(404, {"error": "Video noch nicht vorhanden"})
            try:
                body = file_path.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "video/mp4")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Content-Disposition", f'inline; filename="JALDORX-{job_id}.mp4"')
                self.send_header("Cache-Control", "no-store")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)
                return
            except OSError as exc:
                return self.send_json(500, {"error": f"Video konnte nicht gelesen werden: {exc}"})
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
