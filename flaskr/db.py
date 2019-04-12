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

    # -----------------------------------------------------------------------------
    # Getting a database
    # -----------------------------------------------------------------------------

    db = client.test

    # -----------------------------------------------------------------------------
    # Creating a test document
    # -----------------------------------------------------------------------------

    post = {
        "location": "France",
        "packetNumber": "145sd5"
    }

    # -----------------------------------------------------------------------------
    # Inserting in the mongo database
    # -----------------------------------------------------------------------------

    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    ret = posts.find_one({"Name": "Mansour"})
    del ret["_id"]
    print(ret)
    return dumps(ret)








