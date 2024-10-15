from flask import Blueprint, Response, render_template, request
import time

from .url_base64 import url_safe_base64_decode
from .backend import generate_translate

from .config import server_config

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/translate")
def translate():
    source_text = request.args.get("q")
    source_text = url_safe_base64_decode(source_text)

    def generate():
        try:
            for chunk_message in generate_translate(source_text, server_config):
                yield "data: {}\n\n".format(chunk_message)
        except Exception as e:
            yield "data: {}\n\n".format(str(e))
        yield "event: end\n"
        yield "data: Close the connection.\n\n"

    return Response(generate(), mimetype="text/event-stream")


@bp.route("/echo")
def echo():
    source_text = request.args.get("q")
    source_text = url_safe_base64_decode(source_text)

    def generate():
        for c in source_text:
            yield "data: {}\n\n".format(c)
            time.sleep(0.05)
        yield "event: end\n"
        yield "data: Close the connection.\n\n"

    return Response(generate(), mimetype="text/event-stream")
