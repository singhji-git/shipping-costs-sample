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
    plan = {'9155465072':"Free Roaming", '9572390164':"Free Calling", '919973212':"Free 1GB Data", '9973617212':"30p/min", '91998870950':"Free Videocalling"}
    if req.get("result").get("action") == "current.plan.display":
        result = req.get("result")
        parameters = result.get("parameters")
        number = parameters.get("Phonenumber")
        plan1 = parameters.get("Plan")
        plan[Phonenumber] = plan1
        
    else if req.get("result").get("action") == "current.plan"
        result = req.get("result")
        parameters = result.get("parameters")
        number = parameters.get("Phonenumber")
        comp= parameters.get("Company")
    else
        return {
        "speech": "ok",
        "displayText": "ok1",
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }
        

    speech = "Your current plan of phone no. " + number + " is " + str(plan[number]) + "."

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
