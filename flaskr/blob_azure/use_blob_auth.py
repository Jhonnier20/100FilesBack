import os
import yaml
from azure.storage.blob import ContainerClient
from os import remove


def load_congif():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + "/config.yaml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)


config = load_congif()

local_path = ""


def upload(name, connection_string, container_name):

    try:
        container_client = ContainerClient.from_connection_string(
            connection_string, container_name)

        print('Uploading...')
        blob_client = container_client.get_blob_client(name)
        print("name:", name)

        upload_file_path = os.path.join(local_path, name)

        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)

        remove(upload_file_path)
    except:
        print("Connection Azure Error")


def uploadConnection(name, folder):
    route = ""
    if folder == 1:
        route = config["media_container_name"]
    elif folder == 2:
        route = config["documents_container_name"]

    print(route)
    upload(name,
           config["azure_storage_connectionstring"], route)
