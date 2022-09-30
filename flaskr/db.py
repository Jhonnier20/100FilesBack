import os
from dotenv import load_dotenv
from pymongo import MongoClient, errors

load_dotenv()

try:
    client = MongoClient(os.getenv('MONGOURI'))                   
    db = client['core']
    collection = db['pokes']
    print ('***********  Mongo intance  ***********')
except errors.ServerSelectionTimeoutError as err:
    # do whatever you need
    print(err)

def get_db():
    return db