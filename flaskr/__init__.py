from flask import Flask
import os
from waitress import serve
from flask import abort
from flask import request
from flask import jsonify
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from flaskr.services.functions import upload_file_service, get_files


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Not find page
    @app.errorhandler(404)
    def page_not_found(error):
        abort(404, "wrong path")

    # Test ping
    @app.get("/ping")
    def ping():
        return "<p>pong api version: 0.1</p>"

    @app.errorhandler(Exception)
    def handle_exception(e):
        # pass through HTTP errors
        if isinstance(e, HTTPException):
            return e
        abort(404, "DB connection")

    # Hacemos los api para cargar, y leer los datos de los archivos que hay en la BD

    ALLOWED_EXTENSIONS = set(
        ["png", "jpg", "jpeg", "gif", "pdf", "mp3", "mp4"])

    @app.route('/upload-file', methods=['POST'])
    def upload_file():
        # f = request.form
        # f = f.iterlists()
        # print(len(f))
        request_data = request.get_json()
        upload_file_service(request_data)
        response = {'message': 'success'}
        return jsonify(response)

    @app.get("/get-files")
    def get_files_api():
        return get_files

    return app
