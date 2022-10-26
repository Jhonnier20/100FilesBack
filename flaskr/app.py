from flask import Flask
import os
import socket
from waitress import serve
from flask import abort
from flask import request
from flask import jsonify
from werkzeug.exceptions import HTTPException

from services.functions import upload_file_service, get_files_service, get_storage_service, get_host_service

# Correr Flask: flask --app flaskr --debug run

app = Flask(__name__, instance_relative_config=True)

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

@app.route('/upload-file', methods=['POST'])
def upload_file():
    request_data = request.get_json()
    upload_file_service(request_data)
    response = {'message': socket.gethostname()}
    return jsonify(response)

@app.get("/get-files")
def get_files():
    return get_files_service()

@app.get("/get-storage")
def get_storage():
    return get_storage_service()

@app.get("/get-host")
def get_host():
    return get_host_service()


if __name__ == "__main__":

    port = int(5000)
    app.run(debug=False, host='0.0.0.0', port=port)
