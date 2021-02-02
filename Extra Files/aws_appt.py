#search for patient users
#when the create mtg is called in zoomtest_post, make it call a function here
    #search for patient user to add to this appt by both name and username
    #insert an item into the appt table that has provider name (un), patient name (un), appt time/day, join url
#invite a user to an already created appt? make this a part of edit functionality
#query all appts involving a user by username (provider and patient)
#query user's name from username

import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import json
import datetime

dynamo_client = boto3.client('dynamodb')

def returnAllPatients():
    #dynamodb = boto3.resource("dynamodb", region_name='us-east-1', endpoint_url="http://localhost:4000")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')
    response = table.scan()
    #print( response)

    patientList = []
    for i in response['Items']:
        if i['docStatus']=="patient":
            patientList.append(i['username'])
    
    return patientList

def searchPatientList():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')
    response = table.scan()
    #print( response)

    patientList = []
    for i in response['Items']:
        if i['docStatus']=="patient":
            tmp = ""
            tmp+=i['username']
            tmp+=" - "
            tmp+=i['lname']
            tmp+=", "
            tmp+=i['fname']
            
            patientList.append(tmp)
    
    return patientList

def getAcctFromUsername(username):
    dynamodb = boto3.resource('dynamodb')
    #print(response)
    response = dynamo_client.get_item(TableName= 'users',
            Key={
                'username': {"S":username}
            }
        )
    return response


#TODO improve this implementation (increase efficiency)
def getAllApptsFromUsername(username):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('apptsTable')
    response = table.scan()
    #print(response)
    date_time_str = str(datetime.datetime.now())
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

    todayDate= str(date_time_obj.date())
    apptList = []
    for i in response['Items']:
        if i['provider'] == username or i['patient']==username:
            ##check that the appts happen after the current day (only chack day, not time)
            ##if it's not, delete it (so it doesn't come back up)
            if(todayDate<=i['start_time'][:10]):
                apptList.append(i)
            else:
                deleteApptAWS(i['mtgid'])
    return apptList



def getApptFromMtgId(mtgid):
    mtgid=str(mtgid)
    try:
        response = dynamo_client.get_item(TableName= 'apptsTable',
            Key={
                'mtgid': {"S":mtgid}
            }
        )
        return response
    except ClientError as e:
        print(e.response['Error']['Message'])


def createApptAWS(mtgName, mtgid, provider, patient, start_time, joinURL):
    mtgid=str(mtgid)
    if(len(mtgid)!=11): #does not insert a bad mtgid
        return "THE MTG NUMBER WAS INVALID"
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1', endpoint_url="http://localhost:4000")

    table = dynamodb.Table('YourTestTable')
    dError = True
    pError = True
    try:
        response = dynamo_client.get_item(TableName= 'users',
            Key={
                'username': {"S":provider}
            }
        )
        isDoc=response.get('Item').get('docStatus').get('S')
        if isDoc!="provider":
            return "The provider username sent was not a provider account."
        dError = False
        response = dynamo_client.get_item(TableName= 'users',
            Key={
                'username': {"S":patient}
            }
        )
        try:
            isPat=response.get('Item').get('docStatus').get('S')
        except:
            return "The patient username sent was not a patient account."
        pError = False
    except ClientError as e:
        print(e.response['Error']['Message'])
        if dError:
            print("INVALID DOCTOR NAME.")
            return "You are not valid to create a meeting."
        else:
            print("INVALID PATIENT NAME.")
            return "Error retrieving the account information for patient account."
    #if the provider and patient are both valid

        #error checking the date for extra :00s
    time = str(start_time)
    time = time[:-1] #takes off the 'z'
    if(len(time[11:].split(":"))>=4):
        time = time[:19]
    start_time = time
    
    response = dynamo_client.put_item(TableName= 'apptsTable',
       Item={
            'mtgName':{"S":mtgName},
            'mtgid':{'S':str(mtgid)},
            'provider': {"S":provider},
            'patient': {"S":patient},
            'start_time': {"S":start_time},
            'joinurl':{"S":joinURL}
        }
       )
    return "Successfully inserted the appt into the database."

def deleteApptAWS(mtgid):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('apptsTable')
    mtgID = str(mtgid)
    try:
        response = dynamo_client.delete_item(TableName= 'apptsTable',
            Key={
                'mtgid':{'S':str(mtgid)}
            }
            )
        return "Successfully deleted the meeting."
    except ClientError as e:
        print(e.response['Error']['Message'])
        return "ERROR. Could not delete the meeting."

def updateUserAcct(username, email,fname, lname,password):
    dynamodb = boto3.resource('dynamodb')
    try:
        response = dynamo_client.update_item(TableName= 'users',
            Key={
                'username': {"S":username}
            },
        UpdateExpression="SET #email = :e, #fname=:f, #lname=:l,#password=:p",
        ExpressionAttributeNames= {
        '#email' : 'email',
        '#fname' : 'fname',
        '#lname' : 'lname',
        '#password' : 'password'
    },
    ExpressionAttributeValues= {
        ':e' : {'S':email}, 
        ':f' : {'S':fname},
        ':l' : {'S':lname},
        ':p' : {'S':password}
    },
            ReturnValues="UPDATED_NEW"
        )
        return "Successfully updated user details in the database."
    except ClientError as e:
        print(e.response['Error']['Message'])
        return "ERROR. Could not update the user account."
    return "no"


def updateApptAWS(mtgName, mtgid,start_time): #provider, pat and joinurl(?) will not change
#error checking the date for extra :00s
    mtgid=str(mtgid)
    time = str(start_time)
    time = time[:-1] #takes off the 'z'
    if(len(time[11:].split(":"))>=4):
        time = time[:19]
    start_time = time
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('apptsTable')
    try:
        response = dynamo_client.update_item(TableName= 'apptsTable',
            Key={
                'mtgid':{'S':str(mtgid)}
            },
        UpdateExpression="SET #mtgName = :m, #start_time=:s",
        ExpressionAttributeNames= {
        '#mtgName' : 'mtgName',
        '#start_time' : 'start_time'
    },
    ExpressionAttributeValues= {':m' : {'S':mtgName}, 
        ':s' : {'S':start_time}          
    },
            ReturnValues="UPDATED_NEW"
        )
        return "Successfully updated the appt in the database."
    except ClientError as e:
        print(e.response['Error']['Message'])
        return "ERROR. Could not update the meeting."

def testCal():
    arrOfMtgs =getAllApptsFromUsername('provider1')
    #print(arrOfMtgs)
    mtgList = []#mtgList = jsonResp.get("meetings")
    finalStr = ""
    for item in arrOfMtgs:
        time = str(item.get("start_time"))
        #mtgid = str(item.get("mtgid"))
        if(time[-1]=='Z'):
            time = time[:-1] #takes off the 'z'
        if(len(time[11:].split(":"))>=4):
            time = time[:19]
        end_time = int(float(time[11:13]))+1
        strend = time[:11]+str(end_time)+time[13:]
        if(end_time<=9):
            strend = time[:11]+"0"+str(end_time)+time[13:]
        mtgObj = {"start": time, "end":strend}
        mtgList.append(mtgObj)
    #BADDDD (change this)
    with open('appts.json', 'w') as outfile:
        json.dump(mtgList, outfile)
    with open('appts.json', "r") as input_data:
        #print(input_data.read())
        return input_data.read()

#print(len(getAcctFromUsername('aasdfasd')))
#print(updateUserAcct('provider1', 'testu@gmail.ocm','fake', 'name','d1'))
#print(getAcctFromUsername('provider1'))
#print(getApptFromMtgId(75274348158))
#print(updateApptAWS("NEWTEST", 77353368533, "........"))
#print(getApptFromMtgId(77353368533))
##print(createApptAWS('b', None, 'provider1', 'ads', 'asdf', 'asdf'))
#print(testCal())
