#!/usr/bin/env python3
import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/__save_slide":
            self.send_error(404)
            return
        length = int(self.headers.get("content-length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8"))
        source = payload.get("source", "")
        html = payload.get("html", "")
        target = (Path.cwd() / unquote(source)).resolve()
        root = (Path.cwd() / "sources").resolve()
        if root not in target.parents or not target.name.startswith("slide-") or target.suffix != ".html":
            self.send_error(400, "invalid source")
            return
        target.write_text(html, encoding="utf-8")
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Serving {Path.cwd()} at http://127.0.0.1:{port}/index.html")
    print("Edit mode save endpoint enabled for sources/slide-*.html")
    server.serve_forever()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
