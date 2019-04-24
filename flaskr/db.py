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
def connect(collection):
    client = pymongo.MongoClient(
        "mongodb+srv://Student:MDPESIB2018-2019@iot-cluster-saur7.mongodb.net/test?retryWrites=true",
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE)
    db = client.test
    if(collection=="users"):
        return db.users
    if(collection=="mesureAck100"):
        return db.mesureAck100

    dbcollection = db.posts
    return dbcollection


def sendData():
    post = {
        "location": "Danemark",
        "packetNumber": "145sd5"
    }
    posts="posts"
    collection_instance = connect(posts)
    post_id = collection_instance.insert_one(post).inserted_id

def getData():
    posts = "posts"
    collection_instance = connect(posts)
    data = list(collection_instance.find({"deviceName": "mario"}))
    print(data)
    return dumps(data)

def login(data):
    users="users"
    users_collection=connect(users)
    if users_collection.count_documents({'username': data['username'], 'password':data['password']}, limit=1) != 0:
        return "Success"
    return "Fail"

def get_documents(collection_name):
    mesureAck100="mesureAck100"
    collection= connect(mesureAck100)
    print("hhhhhh")
    l=list(collection.find(({ 'rxInfo.0.time':{'$gt':"2019-04-18T10:57:49.138935Z", '$lt':"2019-04-18T10:59:08.604025Z"}})))
    print(l)
    print(len(l))
    return "ok"

# {'$gte':("2019-04-18T10:57:49.138935Z"),'$lt':("2019-04-18T10:59:08.604025Z")}






