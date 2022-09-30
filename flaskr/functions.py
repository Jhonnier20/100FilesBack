from flaskr.db import get_db
import json
import base64
from file import File

#
# This function calls the database and returns the list with the values of the properties all users in the application.
# This is use to creat the one hot encoding vectors for the cosine similarity analysis
#


def get_pokes():
    db = get_db()
    pokes_collection = db['pokes']
    cursor = pokes_collection.find()

    list_cur = list(cursor)

    for poke in list_cur:
        poke["_id"] = str(poke["_id"])
        # print(poke["_id"])

    return (json.dumps(list_cur))


def add_poke(poke):
    db = get_db()
    pokes_collection = db['pokes']

    x = pokes_collection.insert_one(poke)

    return str(x.inserted_id)


# -----------------------------------------
# DB --> Collection: Files; Documents -> ID, nombre, path, tipo


ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif", "pdf", "mp3", "mp4"])


def save_bucket(data):
    data_decode = base64.decodestring(data)
    return ""


def upload_file(data):
    file_name = data['name']
    ext = file_name.split('.')

    if ext[1] in ALLOWED_EXTENSIONS:
        file_data = data['data']
        path = save_bucket(file_data)

        db = get_db()
        file = File(1, ext[0], path, ext[1])
        files = db['Files']
        files.insert_one(file.getFile())

        return True

    return False


def get_files():
    db = get_db()
    files_collection = db['Files']
    all_files = files_collection.find()
    list_files = list(all_files)

    return list_files
