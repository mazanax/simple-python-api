import ipaddress
from datetime import datetime

from flask import Flask, request, jsonify

app = Flask(__name__)

def is_valid_ip_address(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def get_ip_from_request(req) -> str:
    try:
        ip = req.headers.get("cf-connecting-ip")
        if not ip:
            ip = req.headers.get("x-forwarded-for")
        if not ip:
            ip = req.remote_addr
    except Exception as e:
        raise RuntimeError(f"Cannot get ip from request: {e}")
    return ip if is_valid_ip_address(ip) else ''

def read_file_or_empty(filename: str) -> str:
    try:
        with open(filename, "r") as f:
            return f.read().strip()
    except Exception:
        return ""

@app.route("/")
def index():
    ip = get_ip_from_request(request)
    now = datetime.utcnow().isoformat()
    tag = read_file_or_empty("tag")
    commit = read_file_or_empty("commit")

    return jsonify({
        "time_utc": now,
        "ip": ip,
        "tag": tag,
        "commit": commit
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
