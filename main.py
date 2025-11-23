import os
from flask import Flask, Response, send_from_directory, request
from port import port
from home import home
from template import get_layout
import functools

app = Flask(__name__)


ENV = {}
with open(".env") as f:
    for line in f.readlines():
        if line.strip().startswith("#"):
            continue
        ENV[line.split("=")[0]] = line[line.index("=") + 1 : -1]


def check_auth(username, password):
    return username == ENV["FILE_USERNAME"] and password == ENV["FILE_PASSWORD"]


def authenticate():
    return Response(
        "Login required", 401, {"WWW-Authenticate": 'Basic realm="Protected"'}
    )


def requires_auth(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return wrapper


@app.after_request
def set_default_headers(response: Response):
    # space saving
    response.headers["Server"] = ""
    response.headers["Date"] = ""
    response.headers["Content-Type"] = ""
    return response


@app.route("/")
def home_page():
    return home()


@app.route("/p")
def port_page():
    return port()


@app.errorhandler(404)
def page_not_found(_e):
    return get_layout(lambda: "404")()


@app.route("/files/<path:filename>")
@requires_auth
def file(filename):
    return send_from_directory("./files", filename)


@get_layout
def get_files():
    res = "<style>a{display:block;}</style>"
    root_dir = "./files/"
    for dirpath, dirnames, filenames in os.walk(root_dir):
        rel = os.path.relpath(dirpath, root_dir)
        for f in filenames:
            res += f'<a href="{rel}/{f}">{rel}/{f}</a>'
    return res


@app.route("/files/")
@requires_auth
def files():
    return get_files()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
