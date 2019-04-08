from flask import Flask, request, jsonify
import re
import json
from restaurantHelpers import alreadyAdded, addRestaurant, readFromFile, saveToFile, incrementWeights, removePriority, removeRestaurant, getRestaurantList
from pollHelpers import addVote, grabPoll, endPollHelper, displayVotes, checkPollID, incrementPollID, grabVoting
app = Flask(__name__)

lunchBotToken = '49yjehss5igi8dms95idouncge'
votingSecret = "lunchbotrules"
channel = '39zakunmtfyr9posni4nukj3sy'
inPoll = False

@app.before_first_request
def startup():
    readFromFile()

@app.route("/lunchbot", methods=["POST"])
def lunchbot():
    global channel, lunchBotToken
    req = request.form
    if(lunchBotToken == req.get('token') and channel == req.get('channel_id')):
        command = req.get('text')
        if re.match("add (.+)", command):
            return app.response_class(response=addFood(command[4:]), status=200, mimetype="application/json")
        elif re.match("poll", command):
            return app.response_class(response=gimmeLunch(), status=200, mimetype="application/json")
        elif re.match("list", command):
            print(listRestaurants())
            return app.response_class(response=listRestaurants(), status=200, mimetype="application/json")
        elif re.match("close", command):
            return app.response_class(response=endPoll(), status=200, mimetype="application/json")
        elif re.match("vote", command):
            return app.response_class(response=getVotes(), status=200, mimetype="application/json")
        elif re.match("reset (.+)", command):
            return app.response_class(response=resetRestaurant(command[6:]), status=200, mimetype="application/json")
        elif re.match("remove (.+)", command):
            return app.response_class(response=removeFood(command[7:]), status=200, mimetype="application/json")
        elif re.match("help", command):
            print(listHelp())
            return app.response_class(response=listHelp(), status=200, mimetype="application/json")
        else:
            resp = wrapResponse().format(response_type="ephemeral",data='"type \\"/lunch help\\" for help."')
            return app.response_class(response=resp, status=200, mimetype="application/json")
    else:
        resp = wrapResponse().format(response_type="ephemeral",data='"Forbidden"')
        return app.response_class(response=resp, status=200, mimetype="application/json")

def gimmeLunch():
    global inPoll
    try:
        if(not inPoll):
            inPoll = True
            incrementPollID()
            poll = grabPoll()
            print(poll)
            return poll
        else:
            return wrapResponse().format(response_type="ephemeral", data='"Already deciding what is for lunch."')
    except Exception as e:
        inPoll = False
        return wrapResponse().format(response_type="ephemeral", data='"Error, failed to select a lunch place. Looks like you\'re on your own kid!. {error}"'.format(error=e))

def listRestaurants():
    try:
        test = '"|hi|there|\\n|:-|:-|\\n|1|2|"'
        return wrapResponse().format(response_type="in_channel", data=getRestaurantList())
    except Exception as e:
        print(e)
        return wrapResponse().format(response_type="ephemeral", data='"Error, Cannot list restaurants at this time."')

def addFood(restaurant):
    try:
        newRestaurant = re.match("[a-zA-Z0-9'&]+", restaurant).string
        if(not alreadyAdded(newRestaurant)):
            addRestaurant(newRestaurant)
            return wrapResponse().format(response_type="in_channel", data='"Added {0} from user {1}!"'.format(newRestaurant, request.form.get("user_name")))
        return wrapResponse().format(response_type="ephemeral", data='"It\'s already there!"')
    except Exception as e:
        print(e)
        return wrapResponse().format(response_type="ephemeral", data='"Error, failed to add eatery. Try again later."')

def getVotes():
    if(inPoll):
        return grabVoting()
    else:
        return  wrapResponse().format(response_type="ephemeral", data='"We aren\'t in a poll right now."')

def endPoll():
    global inPoll
    try:
        pollResults = displayVotes()
        winner = endPollHelper()
        removePriority(winner)
        incrementWeights()
        inPoll = False
        return wrapResponse().format(response_type="in_channel", data='"Lunch is at: {place}\\n\\n{poll}"'.format(place=winner, poll=pollResults))
    except:
        return wrapResponse().format(response_type="ephemeral", data='"Error, failed to modify weighting. Try again later."')


def resetRestaurant(rest):
    try:
        restaurant = re.match("[a-zA-Z0-9']+", rest).string
        removePriority(restaurant)
        return wrapResponse().format(response_type="in_channel", data='"Weight reset for {0}. Hope it was good!"'.format(restaurant))
    except Exception as e:
        print(e)
        return wrapResponse().format(response_type="ephemeral", data='"Error, failed to modify weighting. Try again later."')

def removeFood(rest):
    try:
        restaurant = re.match("[a-zA-Z0-9']+", rest).string
        success = removeRestaurant(restaurant)
        if(success):
            return wrapResponse().format(response_type="in_channel", data='"Sad to see {0} go..."'.format(restaurant))
        else:
            return wrapResponse().format(response_type="ephemeral", data='"Restaurant not found."')
    except Exception as e:
        print(e)
        return wrapResponse().format(response_type="ephemeral", data='"Error, failed to remove eatery. Try again later."')

def listHelp():
    helpText = '''"Commands: add restaurant | poll | vote | list | close | reset restaurant | remove restaurant | help"'''
    return wrapResponse().format(response_type="ephemeral", data=helpText)

@app.route("/lunchbot/vote", methods=["POST"])
def vote():
    global votingSecret
    if(votingSecret == request.get_json().get('context').get('secret') and checkPollID(int(request.get_json().get('context').get('pollID')))):
        addVote(request.get_json().get('user_id'), request.get_json().get('context').get('choice'))
        return app.response_class(response='{{"ephemeral_text": "Your vote for {0} has been updated!"}}'.format(request.get_json().get('context').get('choice')), status=200, mimetype="application/json")
    else:
      return app.response_class(response='{"ephemeral_text": "This poll has closed. Please check to see if there is a newer poll"}', status=200, mimetype="application/json")


def wrapResponse():
    return '{{"response_type":"{response_type}", "username":"LunchBot", "icon_url":"https://static-cdn.jtvnw.net/emoticons/v1/1771885/3.0", "text": {data}}}'

if __name__ == '__main__':
 app.run(host="0.0.0.0", port=5000)
