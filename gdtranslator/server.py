from flask import Flask
from flask_cors import CORS
import atexit
import zc.lockfile
import argparse

from .config import server_config

def create_app():
    app = Flask(__name__)
    CORS(app)
    from . import routes

    app.register_blueprint(routes.bp)
    return app


def release_lock(lock):
    lock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="path to config.yaml", type=str)
    args = parser.parse_args()
    config_path = args.config
    server_config.load_server_config_from_yaml(config_path)

    try:
        lock = zc.lockfile.LockFile(server_config.lock_file_path, content_template="{pid}")
        atexit.register(release_lock, lock)
    except zc.lockfile.LockError:
        print("Multiple server instances cannot run simultaneously.")
        exit()

    app = create_app()
    app.run(debug=False)
