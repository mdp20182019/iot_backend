# -----------------------------------------------------------------------------
# All dependencies
# pymongo - dnspython
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# All Imports
# -----------------------------------------------------------------------------

import pymongo
import ssl
import base64
from bson.json_util import dumps
import json


# -----------------------------------------------------------------------------
# Creating a Mongo Client and connecting it to our database
# -----------------------------------------------------------------------------
def connect(collection):
    client = pymongo.MongoClient(
        "mongodb+srv://Student:MDPESIB2018-2019@iot-cluster-saur7.mongodb.net/test?retryWrites=true",
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE)
    db = client.test
    dbcollection = db[collection]
    print("Connected to mongoDb")
    return dbcollection

def getTest():
    client = pymongo.MongoClient(
        "mongodb+srv://Student:MDPESIB2018-2019@iot-cluster-saur7.mongodb.net/test?retryWrites=true",
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE)
    db = client.test
    return db

def sendData():
    post = {
        "location": "Danemark",
        "packetNumber": "145sd5"
    }
    posts="posts"
    collection_instance = connect(posts)
    post_id = collection_instance.insert_one(post).inserted_id

def getHistory():
    collection_instance = getTest()
    collection_instance=collection_instance["history"]
    data = list(collection_instance.find({}))
    for i in data:
        del i['_id']
    data = json.dumps(data)
    return data

def getData():
    posts = "posts"
    collection_instance = connect(posts)
    data = list(collection_instance.find({"deviceName": "mario"}))
    print(data)
    return json.dumps(data)

def login(data):
    users="users"
    users_collection=connect(users)
    if users_collection.count_documents({'username': data['username'], 'password':data['password']}, limit=1) != 0:
        return "Success"
    return "Fail"

def get_documents(collection_name,startDate,endDate,MeasureName,id):
    l=list(collection_name.find(({ 'rxInfo.0.time':{'$gt':startDate, '$lt':endDate}})))
    print(l)
    l = processDocuments(l,MeasureName,id)
    return l


def getMeasureJson(startDate,endDate,MeasureName,id,collectionName):
    collection = connect(collectionName)
    l=get_documents(collection,startDate,endDate,MeasureName,id)
    return l

def statistic(rep,MeasureName):
    dict={0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0}
    for i in rep:
        dict[i]=dict[i]+1
    return {'dict':dict,'saveName':MeasureName+"/stat"}

def packetloss(fcnt,MeasureName):
    fcnt.sort
    j = 0
    i = fcnt[j]
    loss = []
    counter = 0
    while (j < len(fcnt)):
        if (i != fcnt[j]):
            counter += 1
            loss.append(0)
        if (i == fcnt[j]):
            loss.append(1)
            j += 1
        i = i + 1
    counter = counter*100/len(fcnt)
    l={'loss':loss,'pourcentage':counter,'saveName':MeasureName+'/loss'}
    return l


def cleanData(l):
    for i in l:
        del i['_id']
    return l

def getCollectionsUrl():
    nameOfDatabase = getTest()
    collections = nameOfDatabase.list_collection_names()
    return collections

def saveToMongo(data):
    collection = getTest()
    db=collection["history"]
    post_id = db.insert_one(data).inserted_id

def processDocuments(l,MeasureName,id):
    fcnt = []
    rep = []
    j=0
    for i in l:
        if 'fCnt' in i:
            fcnt.append(i['fCnt'])

    while (j < len(l)):
        rep.append(int(base64.b64decode(l[j]['data']).decode('utf-8')))
        j += 1

    stat = statistic(rep,MeasureName)

    packetLoss = packetloss(fcnt,MeasureName)

    l = cleanData(l)
    result = {'data':l,'packetloss':packetLoss,'stat':stat,'identifier':MeasureName+"Data",'id':id}
    result=json.dumps(result)
    print(result)
    return result




