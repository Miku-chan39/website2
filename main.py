from flask import Flask, Response
from port import port
from home import home
from template import get_layout

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
