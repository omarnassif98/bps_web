import socket
from zeroconf import ServiceInfo, Zeroconf
from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__, static_folder=".")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:slug>")
def clean_route(slug):
    # First try to serve directory index (e.g. /contact/ -> /contact/index.html)
    if os.path.isdir(slug) and os.path.exists(os.path.join(slug, "index.html")):
        return send_from_directory(slug, "index.html")

    # Then try slug + ".html" (e.g. /contact -> contact.html)
    html_file = f"{slug}.html"
    if os.path.exists(html_file):
        return send_from_directory(".", html_file)

    # Then try to serve any static file
    if os.path.exists(slug):
        return send_from_directory(".", slug)

    return abort(404)


def start_mdns():
    # Discover local IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    info = ServiceInfo(
        "_http._tcp.local.",
        "flaskserver._http._tcp.local.",
        addresses=[socket.inet_aton(ip)],
        port=5000,
        server="omar.local.",
    )

    zc = Zeroconf()
    zc.register_service(info)
    print(f"Server available at http://omar.local:8000")
    return zc, info

if __name__ == "__main__":
    zc, info = start_mdns()
    try:
        app.run(host='0.0.0.0', port=8000)
    finally:
        zc.unregister_service(info)
        zc.close()