from flask import request
import htmlmin

import re

with open("template.html") as f:
    TEMPLATE = f.read()


def accept_html():
    return "Accept" in request.headers and "html" in request.headers["Accept"]


def get_layout(func, *args):
    def wrapper():
        if accept_html():
            body = TEMPLATE.replace("{body}", func(*args))
            body = htmlmin.minify(body, remove_empty_space=True)
        else:
            body = func(*args)
        print(len(body.encode("utf-8")))
        if len(body.encode("utf-8")) >= 500:
            return "packet too big, please contect admin"
        return body

    return wrapper
