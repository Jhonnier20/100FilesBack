from flask import Flask
import os
import socket
from waitress import serve
from flask import abort
from flask import request
from flask import jsonify
from werkzeug.exceptions import HTTPException
from flask_cors import CORS, cross_origin
from flaskr.services.functions import upload_file_service, get_files_service, get_storage_service, get_host_service

# Correr Flask: flask --app flaskr --debug run


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
    @cross_origin()
    def page_not_found(error):
        abort(404, "wrong path")

    # Test ping
    @app.get("/ping")
    @cross_origin()
    def ping():
        return "<p>pong api version: 0.1</p>"

    @app.errorhandler(Exception)
    @cross_origin()
    def handle_exception(e):
        # pass through HTTP errors
        if isinstance(e, HTTPException):
            return e
        abort(404, "DB connection")

    # Hacemos los api para cargar, y leer los datos de los archivos que hay en la BD

    @app.route('/upload-file', methods=['POST'])
    @cross_origin()
    def upload_file():
        request_data = request.get_json()
        upload_file_service(request_data)
        response = {'message': socket.gethostname()}
        return jsonify(response)

    @app.get("/get-files")
    @cross_origin()
    def get_files():
        return get_files_service()

    @app.get("/get-storage")
    @cross_origin()
    def get_storage():
        return get_storage_service()

    @app.get("/get-host")
    @cross_origin()
    def get_host():
        return get_host_service()

    return app
