import os
from typing import Container
from unittest import result
import yaml
from azure.storage.blob import ContainerClient
from os import remove
from itertools import tee


def load_congif():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + "/config.yaml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)


config = load_congif()

local_path = ""


def storage():
    try:
        tamanio_storage = 0

        # Para la data Media
        container_client = ContainerClient.from_connection_string(
            config["azure_storage_connectionstring"], config["media_container_name"])

        files = container_client.list_blobs()

        for blob in files:
            tamanio_storage = blob["size"]

        container_client = ""
        # Para la data Documents
        container_client = ContainerClient.from_connection_string(
            config["azure_storage_connectionstring"], config["documents_container_name"])

        files = container_client.list_blobs()

        for blob in files:
            tamanio_storage = blob["size"]

        tamanio_storage = tamanio_storage / 1000
        tamanio = {
            'size': round(tamanio_storage, 3),
            'measure': 'MB'
        }

        return tamanio

    except Exception as e:
        print(e)
    return ""


def upload(name, connection_string, container_name):

    try:
        container_client = ContainerClient.from_connection_string(
            connection_string, container_name)

        print('Uploading...')
        blob_client = container_client.get_blob_client(name)
        print("name:", name)

        upload_file_path = os.path.join(local_path, name)
        print(upload_file_path)

        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)

        remove(upload_file_path)
        return "https://bucketexam1.blob.core.windows.net/"

    except Exception as e:
        remove(upload_file_path)
        print(e)


def uploadConnection(name, folder):
    route = ""
    if folder == 1:
        route = config["media_container_name"]
    elif folder == 2:
        route = config["documents_container_name"]

    return upload(name,
                  config["azure_storage_connectionstring"], route)
