# /index.py

from flask import Flask, request, jsonify, render_template, make_response
import os
import dialogflow
import requests
import json
import pusher
from pprint import pprint
import csv
import google.auth.transport.requests
from google.auth import credentials
import requests




#flask app should start in global layout

app = Flask(__name__)
#@app.route('/webhook', methods = ['POST'])
@app.route('/testing', methods = ['GET', 'POST'])


def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request: ")
    print(json.dumps(req, indent=4))

    #res = makeWebHookResult(req)

    res = json.dumps(req, indent=4)
    #print(res)
    r = make_response(res)
    #r.headers['Content-Type'] = 'application/json'

    ### Allows us to write data to file and then use it
    #print(getUtterance(req))
    #print(getActualClassification(req))
    #print(getExpectedClassification())
    #line = getUtterance(req) + getActualClassification(req) + getExpectedClassification()
    writeLine.append(getUtterance(req))
    writeLine.append(getActualClassification(req))
    writeLine.append(getExpectedClassification(req))
    writeLine.append("\n")
    #writeLine.append("\n")

    with open('o1.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(writeLine)
        #1print(writeLine)
            
    with open ('dataJSON.js', 'w') as outfile:
        json.dump(req, outfile)
        print("We did it:)!")
        
    f = open('Johnson_80-20.csv')
    csv_f = csv.reader(f)
    for row in csv_f:
        print(":) :) :)")
        print("row 0: ",row[0])
        print("row 1: ",row[1])
        if (str(row[0]) == getUtterance(req)):
            print(row[0])
            #ec = row[1]
            
    print("finished")
        
    return res

def getUtterance(req):
    utterance = req.get("queryResult").get("queryText")
    return str(utterance)
def getActualClassification(req):
    ac = req.get("queryResult").get("intent").get("displayName")
    acLst = ac.split(" ")
    acInt = int(acLst[1])
    return acInt
def getExpectedClassification(req):
    #ec = -100
    f = open('Johnson_80-20.csv')
    csv_f = csv.reader(f)
    for row in csv_f:
        if str(row[0]) == getUtterance(req):
            #print(row[0])
            ec = row[1]
            return ec
    return -99999
    

def printUserInput(req):
    response = str(req.get("result").get("resolvedQuery"))
    return response

def detect_intent_texts(project_id, session_id, text, language_code):
    
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        #req = request
        print("intent: " + " " + text + " " + str(response.query_result.intent.display_name))
        return str(response.query_result.intent.display_name)

@app.route('/send_message', methods=['POST'])
def send_message():
    google.auth.credentials.expiry = None

    req = request.get_json(silent=True, force=True)
  
    
    
    csv_f = csv.reader(f)
    for row in csv_f:
        
        writeLine = []
        print("row *****: " + str(row))
        target_intent = str(row[1])
        message = str(row[0])
        project_id = "ssg-burch-80-20"
        intent_text = detect_intent_texts(project_id, "testing2", message, 'en')
        strIntent = intent_text.split(" ")
        intent = str(strIntent[1])
        writeLine.append(message)
        writeLine.append(target_intent)
        writeLine.append(str(intent))
        print(writeLine)
        
        
        with open('o1.csv', 'a') as csvfile:
            #writeStr = ",".writeLine
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(writeLine)
        csvfile.close()
            
    print("finished")

    
    return jsonify("Region 1 - high valence, high activation")

if __name__ == "__main__":
    
    writeLine = []
    writeStr = ""
    f = open('b1.csv')
    app.run()


