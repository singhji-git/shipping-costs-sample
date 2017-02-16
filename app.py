#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r



def makeWebhookResult(req):
    x = req.get("result").get("action")
    if  x != "current.plan" and  x != "current.planchange":
        return {}
    
    result = req.get("result")
    parameters = result.get("parameters")
    speech="hey";
    plan = {'9155465072':"Free Roaming", '9572390164':"Free Calling", '919973212':"Free 1GB Data", '9973617212':"30p/min", '91998870950':"Free Videocalling"}
    bill = {'9155465072': 100 , '9572390164': 200 , '919973212': 300 , '9973617212': 350.45 , '91998870950': 345.23 }
    if req.get("result").get("action") == "current.plan":
        number = parameters.get("Phonenumber")
        comp= parameters.get("Company")
        speech = "The cost of shipping to " + number + " is " + str(plan[number]) + "."
    elif req.get("result").get("action") == "current.planchange":
        number = parameters.get("Phonenumber")
        newplan = parameters.get("Plan")
        prevplan = plan[number]
        plan[number] = newplan
        speech = "The plan is changed from  " + prevplan + " to " + str(plan[number]) + "for the " + number + "."
    elif req.get("result").get("action") == "bill.enquiry":
        number = parameters.get("Phonenumber")
        speech = "The bill for   " + number + " is " + str(bill[number]) + "."
        

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }




if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
