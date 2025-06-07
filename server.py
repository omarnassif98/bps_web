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

if __name__ == "__main__":
    app.run(debug=True, port=8000)