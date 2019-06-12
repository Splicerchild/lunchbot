from restaurantHelpers import chooseRandomRestaurant
from userHelpers import getUsername
from uuid import uuid4
import json


choices = []
weights = []
votes = {}
currentPollID = 0

def grabPoll(pretext=''):
    selectChoices()
    return grabVoting(pretext)

def grabVoting(pretext=''):
    global choices, currentPollID
    poll = displayVotes()
    return wrapWithButtons().format(poll=poll, choiceA=choices[0], choiceA2=choices[0], choiceB=choices[1], choiceB2=choices[1], choiceC=choices[2], choiceC2=choices[2], pollID=currentPollID, pretext=pretext)

def addVote(user, vote):
    global votes
    votingTuple = {"vote":vote, "username": getUsername(user)}
    votes[user] = votingTuple

def resetVotes():
    global votes
    votes.clear()

def resetChoices():
    global choices, weights
    choices = []
    weights = []

def getWinner():
    global votes, choices, weights
    tallies = [0, 0, 0]
    for user in votes:
        tallies[choices.index(votes[user]["vote"])] += 1
    if(tallies[0] > tallies[1]):
        if(tallies[0] > tallies[2] or (tallies[0] == tallies[2] and  weights[0] > weights[2])):
            return choices[0]
        else:
            return choices[2]
    elif(tallies[1] > tallies[2] or (tallies[1] == tallies[2] and weights[1] > weights[2])):
        return choices[1]
    else:
        return choices[2]

def selectChoices():
    global choices, weights
    if(len(choices) > 1):
        return
    while (len(choices) < 3):
        choice = chooseRandomRestaurant()
        if(choice['name'] not in choices):
            choices.insert(0, choice['name'])
            weights.insert(0, choice['weight'])

def displayVotes():
    global votes, choices
    tallies = [0,0,0]
    for user in votes:
        tallies[choices.index(votes[user]["vote"])] += 1
    return "|Restaurant|Votes|\\n|:-|:-|\\n|{place1}|{vote1}|\\n|{place2}|{vote2}|\\n|{place3}|{vote3}|".format(place1=choices[0], vote1=tallies[0], place2=choices[1], vote2=tallies[1], place3=choices[2], vote3=tallies[2])

def displayUserVotes():
    global votes
    pollBody = ""
    for user in votes:
        pollBody += "|{name}|{place}|\\n".format(name=votes[user]["username"], place=votes[user]["vote"])
    return "|User|Vote|\\n|:-|:-|\\n{body}".format(body=pollBody)

def endPollHelper():
    winner = getWinner()
    resetVotes()
    resetChoices()
    return winner

def resetPollHelper(user):
    resetVotes()
    resetChoices()
    return grabPoll('Poll reset by {}'.format(user))

def incrementPollID():
    global currentPollID
    currentPollID = uuid4().int

def checkPollID(pollID):
    global currentPollID
    return pollID == currentPollID

def killPollHelper():
    resetVotes()
    resetChoices()

def wrapWithButtons():
    return '''{{"response_type":"in_channel",
        "attachments":[
            {{
                "text":"#### VOTE!\\n{poll}",
                "pretext":"{pretext}",
                "actions":[
                    {{
                        "name": "vote {choiceA}",
                        "integration":{{
                            "url":"http://localhost:5000/lunchbot/vote",
                            "context":{{
                                "choice":"{choiceA2}",
                                "secret":"lunchbotrules",
                                "pollID":"{pollID}"
                            }}
                        }},
                        "type":"button"
                    }},
                    {{
                        "name": "vote {choiceB}",
                        "integration":{{
                            "url":"http://localhost:5000/lunchbot/vote",
                            "context":{{
                                "choice":"{choiceB2}",
                                "secret":"lunchbotrules",
                                "pollID":"{pollID}"
                            }}
                        }},
                        "type":"button"
                    }},
                    {{
                        "name": "vote {choiceC}",
                        "integration":{{
                            "url":"http://localhost:5000/lunchbot/vote",
                            "context":{{
                                "choice":"{choiceC2}",
                                "secret":"lunchbotrules",
                                "pollID":"{pollID}"
                            }}
                        }},
                        "type":"button"
                    }}
                ]
            }}
        ]
    }}'''
