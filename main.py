from flask import Flask, Response, request, redirect
from int2base import int2base
import json

app = Flask(__name__)

url_map = []

map_len = 0

def make_slug():
    global map_len
    map_len += 1
    return int2base(map_len, 36)

def find_item_by(type, value):
    results = [i for i, v in enumerate(url_map) if v[type] == value]
    if len(results) == 0:
        return None
    else:
        return url_map[results[0]]

def url_exists(url):
    for item in url_map:
        if item["url"] == url:
            return True
    return False

def increment_views(slug):
    slugs = [i for i, v in enumerate(url_map) if v["slug"] == slug]
    if len(slugs) > 0:
        url_map[slugs[0]]["views"] += 1


@app.route("/")
def index():
    return "Hello World!"

@app.route("/urls", methods=["POST"])
def urls_post_route():
    if "url" in request.form:
        if not url_exists(request.form["url"]):
            url_map.append({
                "slug": make_slug(),
                "url": request.form["url"],
                "views": 0})
        return Response(json.dumps(find_item_by("url", request.form["url"])), mimetype="application/json")
    else:
        return Response("Error: `url` parameter is required.", mimetype="text/plain", status=500)

@app.route("/urls", methods=["GET"])
def urls_get_route():
    return Response(json.dumps(url_map), mimetype="application/json")

@app.route("/urls/<slug>")
def get_url_route(slug):
    return Response(json.dumps(find_item_by("slug", slug)), mimetype="application/json")

@app.route("/r/<slug>")
def redirect_url_route(slug):
    increment_views(slug)
    return redirect(find_item_by("slug", slug)["url"], code=301)

if __name__ == "__main__":
    app.run()
