import requests
import re
import websocket
import json
import time
import logging
import wsaccel
import sys
ws = websocket.WebSocket()


class s2py():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.headers = {
            "x-csrftoken": "a",
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
            "referer": "https://scratch.mit.edu"
        }
        try:
            data = json.dumps({
                "username": username,
                "password": password
            })
            request = requests.post(
                'https://scratch.mit.edu/login/', data=data, headers=self.headers)
            sessionId = re.search(
                '\"(.*)\"', request.headers['Set-Cookie']).group()
        except AttributeError:
            sys.exit('Error: Invalid credentials. Authentication failed.')
        else:
            self.sessionId = sessionId

    def getStats(id, stat):
        if stat == "loves" or stat == "faves" or stat == "views" or stat == "remixes":
            if stat == "loves":
                r = requests.get(
                    "https://api.scratch.mit.edu/projects/"+str(id))
                data = r.json()
                return data['stats']['loves']
            else:
                if stat == "faves":
                    r = requests.get(
                        "https://api.scratch.mit.edu/projects/"+str(id))
                    data = r.json()
                    return data['stats']['favorites']
                else:
                    if stat == "remixes":
                        r = requests.get(
                            "https://api.scratch.mit.edu/projects/"+str(id))
                        data = r.json()
                        return data['stats']['remixes']
                    else:
                        if stat == "views":
                            r = requests.get(
                                "https://api.scratch.mit.edu/projects/"+str(id))
                            data = r.json()
                            return data['stats']['views']

    def getProjects(user):
        r = requests.get(
            "https://api.scratch.mit.edu/users/"+str(user)+"/projects")
        data = r.json()
        titles = []
        for i in data:
            x = i['title']
            y = i['id']
            titles.append('ID: ' + str(y))
            titles.append('Title: ' + str(x))
        return titles

    def getProjectComments(id):
        uname = requests.get(
            "https://api.scratch.mit.edu/projects/"+str(id)).json()['author']['username']
        data = requests.get("https://api.scratch.mit.edu/users/" +
                            str(uname)+"/projects/"+str(id)+"/comments").json()
        comments = []
        x = ""
        for i in data:
            x = i['content']
            comments.append(x)
        data = json.dumps(comments)
        return data

    def getStudioComments(id):
        r = requests.get(
            "https://api.scratch.mit.edu/studios/"+str(id)+"/comments")
        data = r.json()
        comments = []
        for i in data:
            x = i['content']
            comments.append(x)
        return json.dumps(comments)

    def checkUserExists(user):
        return requests.get("https://api.scratch.mit.edu/accounts/checkusername/"+str(user)).json() == {"username": user, "msg": "username exists"}

    def getUserMessagesCount(user):
        return requests.get("https://api.scratch.mit.edu/users/"+str(user)+"/messages/count").json()['count']

    def getUserFollowerCount(user):
        response = requests.get(
            "https://scratchdb.lefty.one/v3/user/info/"+str(user)).json()
        return response['statistics']['followers']

    def getUserStatus(user):
        return requests.get("https://api.scratch.mit.edu/users/"+str(user)).json()['profile']['status']

    def getUserBio(user):
        return requests.get("https://api.scratch.mit.edu/users/"+str(user)).json()['profile']['bio']

    def setCloudVar(self, variable, value):
        try:
            sendPacket({
                'method': 'set',
                'name': '☁ ' + variable,
                'value': str(value),
                'user': self.username,
                'project_id': str(PROJECT_ID)
            })
            time.sleep(0.1)
        except BrokenPipeError:
            logging.error('Broken Pipe Error. Connection Lost.')
            ws.connect('wss://clouddata.scratch.mit.edu', cookie='scratchsessionsid='+self.sessionId+';',
                       origin='https://scratch.mit.edu', enable_multithread=True)
            sendPacket({
                'method': 'handshake',
                'user': self.username,
                'project_id': str(PROJECT_ID)
            })
            time.sleep(0.1)
            logging.info('Re-connected to wss://clouddata.scratch.mit.edu')

    def readCloudVar(name, limit=""):
        if limit == "":
            limit = 1000
        resp = requests.get("https://clouddata.scratch.mit.edu/logs?projectid=" +
                            str(PROJECT_ID)+"&limit="+str(limit)+"&offset=0").json()
        for i in resp:
            x = i['name']
            if x == ('☁ ' + str(name)):
                return i['value']

    def cloudConnect(self, pid):
        global ws
        global PROJECT_ID
        PROJECT_ID = pid
        ws.connect('wss://clouddata.scratch.mit.edu', cookie='scratchsessionsid='+self.sessionId+';',
                   origin='https://scratch.mit.edu', enable_multithread=True)
        sendPacket({
            'method': 'handshake',
            'user': self.username,
            'project_id': str(pid)
        })


def sendPacket(packet):
    ws.send(json.dumps(packet) + '\n')
