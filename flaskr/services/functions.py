from database.db import get_db
import json
import base64
from model.file import File
from blob_azure.use_blob_auth import uploadConnection, storage
from werkzeug.utils import secure_filename
import os
import socket

#
# This function calls the database and returns the list with the values of the properties all users in the application.
# This is use to creat the one hot encoding vectors for the cosine similarity analysis
#


# def get_pokes():
#     db = get_db()
#     pokes_collection = db['pokes']
#     cursor = pokes_collection.find()

#     list_cur = list(cursor)

#     for poke in list_cur:
#         poke["_id"] = str(poke["_id"])
#         # print(poke["_id"])

#     return (json.dumps(list_cur))

# -----------------------------------------
# DB --> Collection: Files; Documents -> ID, nombre, path, tipo

# Tipo de extensiones que aceptaremos. Lo dividimos en media y documents porque en el storage account de Azure está subdividido
DOCUMENT_EXTENSIONS = set(["pdf", "docx", "csv", "xlsx", "pptx"])
MEDIA_EXTENSIONS = set(["png", "jpg", "jpeg", "gif", "mp3", "mp4"])


# Metodo para decodificar la data y guardarla en el server y luego llamar al uploadConnection para enviar al azure
# recibimos data en base64
# nombre completo del archivo
# type = 1 es tipo media, type = 2 es tipo documento
def save_bucket(data, fullname, type):
    data_decode = base64.b64decode(data)
    with open(fullname, "wb") as f:
        file = f.write(data_decode)

    return uploadConnection(fullname, type)


# Metodo que recibe el json data con dos atributos.
# 'name' nombre completo del archivo
# 'data' data en base 64 del archivo
# Aqui evaluamos si es media o document y luego guardamos la informacion del file en la bd
def upload_file_service(data):
    try:
        file_name = data['name']
        ext = file_name.split(".")
        path = ""

        if ext[1] in MEDIA_EXTENSIONS:
            file_data = data['data']
            path = save_bucket(file_data, file_name, 1)
            path = path + "media/" + file_name

        elif ext[1] in DOCUMENT_EXTENSIONS:
            file_data = data['data']
            path = save_bucket(file_data, file_name, 2)
            path = path + "documents/" + file_name

        else:
            return False

        if path != "":
            db = get_db()
            file = File(id="", name=ext[0], path=path, ext=ext[1])
            print(file)
            collection = db['Files']
            collection.insert_one(file.getFile())

            return True

        else:
            return False

    except Exception as e:
        print(e)


# Metodo para retornar la lista de Files que hay en la BD
# Return un json con la lista
def get_files_service():
    db = get_db()
    files_collection = db['Files']
    all_files = files_collection.find()

    list_files = list(all_files)

    for file in list_files:
        file["_id"] = str(file["_id"])

    return (json.dumps(list_files))


def get_storage_service():
    return storage()


def get_host_service():
    host = {
        'name': socket.gethostname(),
        'ip': socket.gethostbyname(socket.gethostname())
    }
    return host
