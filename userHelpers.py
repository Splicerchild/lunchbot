import json

saveFile = "/home/ubuntu/lunchbot/users.json"
userList = {}

def isValidUser(userInfo):
    global userList
    return userInfo["id"] in userList

def getUserInfo(request):
    return  {"name":request.form.get('user_name'), "id":request.form.get('user_id')}

def registerUserToList(userInfo):
    global userList
    userList[userInfo["id"]] = userInfo
    saveToFile()

def getUsername(userID):
    global userList
    return userList[userID]["name"]

def readUsersFromFile():
    global userList, saveFile
    try:
        file = open(saveFile, 'r')
        userList = json.loads(file.read())
    except:
        print("failed to load from file; creating new user array")
        userList = {}


def saveToFile():
    global userList, saveFile
    file = open(saveFile, 'w')
    file.write(json.dumps(userList))
    file.close()
