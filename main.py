from flask import Flask, Response, request
from int2base import int2base
import json

app = Flask(__name__)

url_map = {}
map_len = 0

def make_slug(url):
    global map_len
    map_len += 1
    return int2base(map_len, 36)

def get_slug(url):
    list(url_map.keys())[list(url_map.values()).index(url)]

@app.route("/")
def index():
    return "Hello World!"

@app.route("/urls", methods=["GET", "POST"])
def urls():
    if request.method == "POST":
        if "url" in request.form:
            if request.form["url"] not in url_map.values():
                url_map[make_slug(request.form["url"])] = request.form["url"]
            return Response(json.dumps({"url": request.form["url"], "slug": get_slug(request.form["url"])}), mimetype="application/json")
        else:
            return Response("Error: `url` parameter is required.", mimetype="text/plain", status=500)
    else:
        return Response(json.dumps(url_map), mimetype="application/json")

@app.route("/urls/<slug>")
def get_url(slug):
    response = {
            "url": url_map[slug],
            "slug": slug
    }
    return Response(json.dumps(response), mimetype="application/json")

if __name__ == "__main__":
    app.run()
