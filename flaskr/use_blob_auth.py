import os
import yaml
from azure.storage.blob import ContainerClient


def load_congif():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + "/config.yaml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)


config = load_congif()


def upload(file, connection_string, container_name):
    container_client = ContainerClient.from_connection_string(
        connection_string, container_name)
    print('Uploading...')
    blob_client = container_client.get_blob_client("hi.txt")
    blob_client.upload_blob(file)


upload("/flaskr/data.txt",
       config["azure_storage_connectionstring"], config["documents_container_name"])
