import json
import random
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


def estimate_pi_monte_carlo(num_samples=1000000):
    if num_samples <= 0:
        raise ValueError("num_samples is invalid")
    inside_circle = 0
    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1.0:
            inside_circle += 1
    return (4.0 * inside_circle) / num_samples


def stress_cpu(seconds=2.0):
    start = time.time()
    while time.time() - start < seconds:
        _ = 1000 * 1000
    return round(time.time() - start, 3)


def stress_memory(mb=50):
    data = bytearray(mb * 1024 * 1024)
    time.sleep(1.0)
    del data
    return mb


class ChaosProbeHandler(BaseHTTPRequestHandler):

    def send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/health":
            self.send_json_response(200, {
                "status": "healthy",
                "service": "chaos-probe-live"
            })
        elif path == "/estimate-pi":
            samples = 1000000
            if "samples" in params:
                try:
                    samples = int(params["samples"][0])
                except ValueError:
                    self.send_json_response(400, {"error": "Invalid samples"})
                    return
            t0 = time.time()
            pi = estimate_pi_monte_carlo(samples)
            elapsed = round(time.time() - t0, 4)
            self.send_json_response(200, {
                "algorithm": "monte_carlo",
                "samples": samples,
                "estimated_pi": pi,
                "elapsed_seconds": elapsed
            })
        elif path == "/stress/cpu":
            seconds = 2.0
            if "seconds" in params:
                try:
                    seconds = float(params["seconds"][0])
                except ValueError:
                    self.send_json_response(400, {"error": "Invalid seconds"})
                    return
            actual_seconds = stress_cpu(seconds)
            self.send_json_response(200, {
                "status": "completed",
                "target_seconds": seconds,
                "actual_seconds": actual_seconds
            })
        elif path == "/stress/memory":
            mb = 50
            if "mb" in params:
                try:
                    mb = int(params["mb"][0])
                except ValueError:
                    self.send_json_response(400, {"error": "Invalid mb"})
                    return
            allocated_mb = stress_memory(mb)
            self.send_json_response(200, {
                "status": "completed",
                "allocated_mb": allocated_mb
            })
        elif path == "/":
            self.send_json_response(200, {
                "service": "DevOps Chaos & Telemetry Probe",
                "endpoints": [
                    "/health",
                    "/estimate-pi?samples=1000000",
                    "/stress/cpu?seconds=2.0",
                    "/stress/memory?mb=50"
                ]
            })
        else:
            self.send_json_response(404, {"error": "Endpoint not found"})


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    server = HTTPServer((host, port), ChaosProbeHandler)
    print(f"🚀 Server running on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server gracefully...")
        server.server_close()
