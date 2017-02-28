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


import urllib
import time


class Voicent:
    def __init__(self, host="localhost", port="8155"):
    self.host_ = host
    self.port_ = port

    def callText(self, phoneno, text, selfdelete):
    urlstr = "/ocall/callreqHandler.jsp"

    param = {'info' : 'simple text call',
             'phoneno' : phoneno,
             'firstocc' : 10,
             'txt' : text,
             'selfdelete' : selfdelete}

    rcstr = self.postToGateway(urlstr, param)
    return self.getReqId(rcstr)

    def callAudio(self, phoneno, filename, selfdelete):
        urlstr = "/ocall/callreqHandler.jsp"

        param = {'info' : 'simple audio call',
             'phoneno' : phoneno,
             'firstocc' : 10,
             'audiofile' : filename,
             'selfdelete' : selfdelete}

        rcstr = self.postToGateway(urlstr, param)
        return self.getReqId(rcstr)

    def callStatus(self, reqId):
        urlstr = "/ocall/callstatusHandler.jsp"
        param = {'reqid' : reqId}
        rcstr = self.postToGateway(urlstr, param)

        if (rcstr.find("^made^") != -1):
              return "Call Made"

        if (rcstr.find("^failed^") != -1):
            return "Call Failed"

        if (rcstr.find("^retry^") != -1):
            return "Call Will Retry"

        return ""

    def callRemove(self, reqId):
        urlstr = "/ocall/callremoveHandler.jsp"
        param = {'reqid' : reqId}
        rcstr = self.postToGateway(urlstr, param)
    def callTillConfirm(self, vcastexe, vocfile, wavfile, ccode):
        urlstr = "/ocall/callreqHandler.jsp"

        cmdline = "\""
        cmdline += vocfile
        cmdline += "\""
        cmdline += " -startnow"
        cmdline += " -confirmcode "
        cmdline += ccode
        cmdline += " -wavfile "
        cmdline += "\""
        cmdline += wavfile
        cmdline += "\""

    param = {'info' : 'Simple Call till Confirm',
             'phoneno' : '1111111',
             'firstocc' : 10,
             'selfdelete' : 0,
             'startexec' : vcastexe,
             'cmdline' : cmdline}

    self.postToGateway(urlstr, param)


    def postToGateway(self, urlstr, poststr):
        params = urllib.urlencode(poststr)
        url = "http://" + self.host_ + ":" + self.port_ + urlstr
        f = urllib.urlopen(url, params)
        return f.read()

    def getReqId(self, rcstr):
        index1 = rcstr.find("[ReqId=")
        if (index1 == -1):
            return ""
        index1 += 7

        index2 = rcstr.find("]", index1)
        if (index2 == -1):
            return ""

        return rcstr[index1:index2]



#
# Uncomment out the following for your test
#
#put your own number there
#phoneno = "111-2222"
#
#v = Voicent()
#v.callText(phoneno, "hello, how are you", "1")

#reqid = v.callAudio(phoneno, "C:/Program Files/Voicent/MyRecordings/sample_message.wav", "0")

#while (1):
# time.sleep(1)
# status = v.callStatus(reqid)
# if (status != ""):
# break

#v.callRemove(reqid)

#v.callTillConfirm("C:/Program Files/Voicent/BroadcastByPhone/bin/vcast.exe",
# "C:/temp/testctf.voc",
# "C:/Program Files/Voicent/MyRecordings/sample_message.wav",
# "1234")




def makeWebhookResult(req):
    x = req.get("result").get("action")
#     if  x != "current.plan" and  (x != "current.planchange" and x != "bill.enquiry"):
#         return {}
    
    result = req.get("result")
    parameters = result.get("parameters")
    speech="hey";
    plan = {'9155465072':"Free Roaming", '9572390164':"Free Calling", '919973212':"Free 1GB Data", '9973617212':"30p/min", '91998870950':"Free Videocalling"}
    bill = {'9155465072': "100" , '9572390164': "200" , '919973212': "300" , '9973617212': "350.45" , '91998870950': "345.23" }
    subscription = {'9155465072': "callerTuneActivated" , '9572390164': "none" , '919973212': "callerTuneActivated" , '9973617212': "none" , '91998870950': "callerTuneActivated" }
    if req.get("result").get("action") == "current.plan":
        number = parameters.get("Phonenumber")
        comp= parameters.get("Company")
        speech = "The current plan of the user with phone no. " + number + " is " + str(plan[number]) + "."
    elif req.get("result").get("action") == "current.planchange":
        number = parameters.get("Phonenumber")
        newplan = parameters.get("Plan")
        prevplan = plan[number]
        plan[number] = newplan
        speech = "The plan is changed from  " + prevplan + " to " + str(plan[number]) + "for the " + number + "."
    elif req.get("result").get("action") == "bill.enquiry":
        number = parameters.get("Phonenumber")
        speech = "The bill for   " + number + " is " + str(bill[number]) + "."
    elif req.get("result").get("action") == "bill.highcomplain" :
        number = parameters.get("Phonenumber")
        subscription1 = subscription[number]
        if subscription1 == "none" :
            speech = "you phone no. " + number + " is not subscribed for any featues.."
        else :
            speech = "you phone no. " + number + " is  subscribed to " + subscription1 + ". do you want to unsubsribe.."
            
#     elif req.get("result").get("action") == "subscription.yes" :
#         number = parameters.get("Phonenumber")
#         speech = "you have been unsubscribed for the feature" + subscription[number] +"."
#         subscription[number] = "none"
        
    else :
        callText(9155465072, "hey are you getting a call", selfdelete)
        speech = "hey1"
        

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
