from flask import request
from template import get_layout, accept_html
import random


@get_layout
def port():
    start = 10000
    try:
        start = int(request.args.get("s", "10000"))
    except ValueError:
        pass
    end = 65535
    try:
        end = int(request.args.get("e", "65535"))
    except ValueError:
        pass
    end, start = max(start, end), min(start, end)
    port = random.randint(start, end)

    if accept_html():
        return f'A random port from range {start}~{end} (set range by ?s=[start]&e=[end]) : <p style="color:red">{port}</p> '
    return port
