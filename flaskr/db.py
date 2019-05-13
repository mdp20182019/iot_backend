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
import statistics
import json

list_of_Measure_collections=["NoAckL","NoAckM","NoAckH","AckL","AckL","AckL","RedL","RedM","RedH"]
l=['NoAckL','NoAckM','NoAckH','AckL','AckM','AckH','RedL','RedM','RedH']


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


def getHistory():
    collection_instance = getTest()
    collection_instance=collection_instance["history"]
    data = list(collection_instance.find({}))
    for i in data:
        del i['_id']
    data = json.dumps(data)
    return data


def login(data):
    users="users"
    users_collection=connect(users)
    if users_collection.count_documents({'username': data['username'], 'password':data['password']}, limit=1) != 0:
        return "Success"
    return "Fail"

def get_documents(collection_name,startDate,endDate,MeasureName,id):
    l=list(collection_name.find(({ 'rxInfo.0.time':{'$gt':startDate, '$lt':endDate}})))
    # print(l)
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
    l={'loss':loss,'saveName':MeasureName+'/loss'}
    return l

def packetlossForMainMeasure(fcnt):
    return (900-len(fcnt))/9

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
    print(len(l))

    while (j < len(l)):
        rep.append(int(base64.b64decode(l[j]['data']).decode('utf-8')))
        j += 1

    stat = statistic(rep,MeasureName)
    dicto=packetloss(fcnt,MeasureName)
    packetLoss = packetlossForMainMeasure(fcnt)
    dicto['pourcentage']=packetLoss

    l = cleanData(l)
    result = {'data':l,'packetloss':dicto,'stat':stat,'identifier':MeasureName+"Data",'id':id}
    result=json.dumps(result)
    # print(result)
    return result


def getMainMeasureDataReturn(data):
    return treatLists(getMainMeasureData(data))


###########################################################################################################
# Main Measure components


def getDocuments(start,end,collection):
    return list(collection.find(({ 'rxInfo.0.time':{'$gt':start, '$lt':end}})))


def getFcnt(l):
    fcnt=[]
    for i in l:
        if 'fCnt' in i:
            fcnt.append(i['fCnt'])
    return fcnt

def getMainMeasureData(data):
    TotalFcnt=[]
    for i in list_of_Measure_collections:
        collection = connect(i)
        if(i=="Redund100Sf10" or i=="Redund100Sf10" or i=="Redund100Sf10"):
            l=getDocuments(data['startDate_Ack'],data['endDate_Ack'],collection)
        elif(i=="Redund50Sf10" or i=="Redund50Sf10" or i=="Redund50Sf10"):
            l=getDocuments(data['startDate_NoAck'],data['endDate_NoAck'],collection)
        else:
            l=getDocuments(data['startDate_Red'],data['endDate_Red'],collection)
        TotalFcnt.append(l)
    return TotalFcnt

def treatLists(l):
    ll=[]
    lll=[]
    llll=[]
    dict={}
    for sublist in l:
        lll.append((get_packet_count(sublist)))
        llll.append(repetition(sublist))
    for sublist in l:
        sublist= getFcnt(sublist)
        ll.append(minMaxMedianne(getStats(createBatches(sublist))))
    dict['stats']=ll
    dict['count']=lll
    dict['repetition']=llll
    return dict

def get_packet_count(l):
    res= {}
    res['totalReceived'] = len(l)
    return res

def repetition(l):
    j=0
    count=0
    while (j < len(l)):
        count=count+int(base64.b64decode(l[j]['data']).decode('utf-8'))
        j += 1
    return count


def createBatches(l):
    final=[]
    ll=[]
    size=30
    for i in l:
        if(i>size and i<900 and i>0):
            size+=30
            final.append(ll)
            ll=[]
            ll.append(i)
        elif(i<900 and i>0):
            ll.append(i)
    final.append(ll)
    return final


def getStats(l):
    lll=[]
    for subList in l:
        gain=len(subList)*100/30
        lll.append(gain)
    return lll



def minMaxMedianne(l):
    if(type(l)==float):
            ll={}
            ll['min']=l
            ll['max']=l
            ll['median']=l
            ll['mean']=l
            ll['pstdev']=l
            return ll
    else:
            ll={}
            ll['min']=min(l)
            ll['max']=max(l)
            ll['median']=statistics.median(l)
            ll['mean']=statistics.mean(l)
            ll['pstdev']=statistics.pstdev(l)
            return ll

###########################################################################################################



