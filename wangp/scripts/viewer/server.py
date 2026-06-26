#!/usr/bin/env python3
"""Wan2AI Image Gallery Server — serves generated images with live refresh."""

import argparse
import base64
import json
import mimetypes
import os
import socket
import sys
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

WS_MAGIC = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


class GalleryHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, gallery_dir=None, state_dir=None, **kwargs):
        self.gallery_dir = gallery_dir
        self.state_dir = state_dir
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self._serve_index()
        elif self.path == "/api/images":
            self._serve_images_list()
        elif self.path.startswith("/image/"):
            self._serve_image()
        elif self.path == "/api/watch":
            self._serve_watch()
        else:
            self.send_error(404)

    def _serve_index(self):
        template_path = Path(__file__).parent / "gallery.html"
        html = template_path.read_text()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(html.encode())

    def _serve_images_list(self):
        images = self._scan_images()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(images).encode())

    def _serve_image(self):
        filename = self.path[7:]  # strip /image/
        filepath = self.gallery_dir / filename
        if not filepath.exists():
            self.send_error(404)
            return
        content_type, _ = mimetypes.guess_type(str(filepath))
        if not content_type:
            content_type = "image/jpeg"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(filepath.read_bytes())

    def _serve_watch(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Connection", "keep-alive")
        self.end_headers()

        last_count = 0
        try:
            while True:
                images = self._scan_images()
                if len(images) != last_count:
                    data = json.dumps({"type": "update", "count": len(images), "latest": images[0] if images else None})
                    self.wfile.write(f"data: {data}\n\n".encode())
                    self.wfile.flush()
                    last_count = len(images)
                time.sleep(1)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _scan_images(self):
        exts = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}
        images = []
        for f in self.gallery_dir.iterdir():
            if f.is_file() and f.suffix.lower() in exts:
                images.append({
                    "name": f.name,
                    "url": f"/image/{f.name}",
                    "mtime": f.stat().st_mtime,
                    "size": f.stat().st_size,
                })
        images.sort(key=lambda x: x["mtime"], reverse=True)
        return images


def run_server(gallery_dir, port, host="127.0.0.1"):
    gallery_dir = Path(gallery_dir).resolve()
    gallery_dir.mkdir(parents=True, exist_ok=True)

    state_dir = gallery_dir.parent / ".viewer-state"
    state_dir.mkdir(parents=True, exist_ok=True)

    handler = lambda *args, **kwargs: GalleryHandler(*args, gallery_dir=gallery_dir, state_dir=state_dir, **kwargs)
    server = HTTPServer((host, port), handler)

    server_info = {
        "type": "server-started",
        "port": port,
        "host": host,
        "url": f"http://{host}:{port}",
        "gallery_dir": str(gallery_dir),
        "state_dir": str(state_dir),
        "pid": os.getpid(),
    }

    info_path = state_dir / "server-info"
    info_path.write_text(json.dumps(server_info))

    print(json.dumps(server_info), flush=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        stopped_path = state_dir / "server-stopped"
        stopped_path.write_text(json.dumps({"type": "server-stopped", "time": time.time()}))


def main():
    parser = argparse.ArgumentParser(description="Wan2AI Image Gallery Server")
    parser.add_argument("--gallery-dir", required=True, help="Directory to watch for images")
    parser.add_argument("--port", type=int, default=0, help="Port (0 = auto)")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind")
    args = parser.parse_args()

    if args.port == 0:
        args.port = find_free_port()

    run_server(args.gallery_dir, args.port, args.host)


if __name__ == "__main__":
    main()
