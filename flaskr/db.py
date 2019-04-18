# -----------------------------------------------------------------------------
# All dependencies
# pymongo - dnspython
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# All Imports
# -----------------------------------------------------------------------------

import pymongo
import ssl
from bson.json_util import dumps


# -----------------------------------------------------------------------------
# Creating a Mongo Client and connecting it to our database
# -----------------------------------------------------------------------------
def connect():
    client = pymongo.MongoClient(
        "mongodb+srv://Student:MDPESIB2018-2019@iot-cluster-saur7.mongodb.net/test?retryWrites=true",
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE)
    print("Connected to mongo")

    db = client.test

    posts = db.posts
    return posts


def sendData():
    post = {
        "location": "Danemark",
        "packetNumber": "145sd5"
    }
    collection_instance = connect()
    post_id = collection_instance.insert_one(post).inserted_id

def getData():
    collection_instance = connect()
    data = list(collection_instance.find({"deviceName": "mario"}))
    print(data)
    return dumps(data)



