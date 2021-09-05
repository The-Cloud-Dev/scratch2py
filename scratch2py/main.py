import requests
import re
import websocket
import json
import time
import logging
import sys
import json
import ScratchEncoder
ws = websocket.WebSocket()
encoder = ScratchEncoder.Encoder()


class s2py():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.headers = {
            "x-csrftoken": "a",
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
            "referer": "https://scratch.mit.edu",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
        }
        try:
            data = json.dumps({
                "username": username,
                "password": password
            })
            request = requests.post(
                'https://scratch.mit.edu/login/', data=data, headers=self.headers)
            self.sessionId = re.search(
                '\"(.*)\"', request.headers['Set-Cookie']).group()
            self.token = request.json()[0]["token"]
            headers = {
                "x-requested-with": "XMLHttpRequest",
                "Cookie": "scratchlanguage=en;permissions=%7B%7D;",
                "referer": "https://scratch.mit.edu",
            }
            request = requests.get(
                "https://scratch.mit.edu/csrf_token/", headers=headers)
            self.csrftoken = re.search(
                "scratchcsrftoken=(.*?);", request.headers["Set-Cookie"]
            ).group(1)

        except AttributeError:
            sys.exit('Error: Invalid credentials. Authentication failed.')
        else:
            self.headers = {
                "x-csrftoken": self.csrftoken,
                "X-Token": self.token,
                "x-requested-with": "XMLHttpRequest",
                "Cookie": "scratchcsrftoken="
                + self.csrftoken
                + ";scratchlanguage=en;scratchsessionsid="
                + self.sessionId
                + ";",
                "referer": "",
            }

    def decode(self, text):
        return encoder.decode(text)
    
    def encode(self, text):
        return encoder.encode(text)
    
    def getStats(self, id, stat):
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

    def getProjects(self, user):
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

    def getProjectComments(self, id):
        uname = requests.get(
            "https://api.scratch.mit.edu/projects/"+str(id)).json()
        if uname != {"code": "NotFound", "message": ""}:
            uname = uname['author']['username']
            data = requests.get("https://api.scratch.mit.edu/users/" +
                                str(uname)+"/projects/"+str(id)+"/comments").json()
            comments = []
            if data != {"code": "ResourceNotFound", "message": "/users/"+str(uname)+"/projects/175/comments does not exist"} and data != {"code": "NotFound", "message": ""}:
                x = ""
                for i in data:
                    if "content" in i:
                        x = i['content']
                    else:
                        if "image" in i:
                            x = i['image']
                        else:
                            x = "None"
                    comments.append(str('Username: '+str(uname))+(str(', Content: ')+str(x)))
                return data

    def inviteCurator(self, sid, user):
        self.headers["referer"] = (
            "https://scratch.mit.edu/studios/" + str(sid) + "/curators/")
        requests.put("https://scratch.mit.edu/site-api/users/curators-in/" +
                     str(sid) + "/invite_curator/?usernames=" + user, headers=self.headers,)

    def shareProject(self, pid):
        self.headers["referer"] = (
            "https://scratch.mit.edu/projects/"+str(pid)
        )
        return requests.put("https://api.scratch.mit.edu/proxy/projects/"+str(pid)+"/share",headers=self.headers)
    
    def unshareProject(self, pid):
        self.headers["referer"] = (
            "https://scratch.mit.edu/projects/"+str(pid)
        )
        return requests.put("https://api.scratch.mit.edu/proxy/projects/"+str(pid)+"/unshare",headers=self.headers)
    
    def postStudioComment(self, sid, content, parent_id="", commentee_id=""):
        self.headers['referer'] = (
            "https://scratch.mit.edu/studios/" + str(sid) + "/comments/"
        )
        data = {
            "commentee_id": commentee_id,
            "content": content,
            "parent_id": parent_id,
        }
        return requests.post(
            "https://scratch.mit.edu/site-api/comments/gallery/"
            + str(sid)
            + "/add/",
            headers=self.headers,
            data=json.dumps(data),
        )

    def favorite(self, id):
        self.headers['referer'] = "https://scratch.mit.edu/projects/"+str(id)
        return requests.post(
            "https://api.scratch.mit.edu/proxy/projects/"
            + str(id)
            + "/favorites/user/"
            + self.username,
            headers=self.headers,
        ).json()

    def addStudioProject(self, sid, pid):
        self.headers['referer'] = "https://scratch.mit.edu/projects/"+str(pid)
        return requests.post("https://api.scratch.mit.edu/studios/"+str(sid)+"/project/"+str(pid), headers=self.headers)

    def unfavorite(self, id):
        self.headers['referer'] = "https://scratch.mit.edu/projects/"+str(id)
        return requests.delete(
            "https://api.scratch.mit.edu/proxy/projects/"
            + str(id)
            + "/favorites/user/"
            + self.username,
            headers=self.headers,
        ).json()

    def love(self, id):
        self.headers['referer'] = "https://scratch.mit.edu/projects/"+str(id)
        return requests.post(
            "https://api.scratch.mit.edu/proxy/projects/"
            + str(id)
            + "/loves/user/"
            + self.username,
            headers=self.headers,
        ).json()

    def unlove(self, id):
        self.headers['referer'] = "https://scratch.mit.edu/projects/"+str(id)
        return requests.delete(
            "https://api.scratch.mit.edu/proxy/projects/"
            + str(id)
            + "/loves/user/"
            + self.username,
            headers=self.headers,
        ).json()

    def followStudio(self, id):
        self.headers['referer'] = "https://scratch.mit.edu/studios/"+str(id)
        return requests.put(
            "https://scratch.mit.edu/site-api/users/bookmarkers/"
            + str(id)
            + "/remove/?usernames="
            + self.username,
            headers=self.headers,
        ).json()

    def unfollowStudio(self, id):
        self.headers['referer'] = "https://scratch.mit.edu/studios/"+str(id)
        return requests.put(
            "https://scratch.mit.edu/site-api/users/bookmarkers/"
            + str(id)
            + "/remove/?usernames="
            + self.username,
            headers=self.headers,
        ).json()

    def getStudioComments(self, id):
        r = requests.get(
            "https://api.scratch.mit.edu/studios/"+str(id)+"/comments")
        data = r.json()
        comments = []
        for i in data:
            x = i['content']
            comments.append(x)
        return json.dumps(comments)

    def followUser(self, username):
        self.headers['referer'] = "https://scratch.mit.edu/users/" + \
            str(username)+"/"
        return requests.put(
            "https://scratch.mit.edu/site-api/users/followers/"
            + username
            + "/add/?usernames="
            + self.username,
            headers=self.headers,
        ).json()

    def unfollowUser(self, username):
        self.headers['referer'] = "https://scratch.mit.edu/users/" + \
            str(username)+"/"
        return requests.put(
            "https://scratch.mit.edu/site-api/users/followers/"
            + self.username
            + "/remove/?usernames="
            + username,
            headers=self.headers,
        ).json()


    def toggleCommenting(self):
        self.headers['referer'] = "https://scratch.mit.edu/users/" + \
            str(self.username)
        return requests.post(
            "https://scratch.mit.edu/site-api/comments/user/" +
            str(self.username)+"/toggle-comments/",
            headers=self.headers,
        )

    def unfollowPost(self, postid):
        self.headers['referer'] = "https://scratch.mit.edu/discuss/topic/" + \
            str(postid)
        return requests.post("https://scratch.mit.edu/discuss/subscription/topic/"+str(postid)+"/delete/", headers=self.headers)

    def followPost(self, postid):
        self.headers['referer'] = "https://scratch.mit.edu/discuss/topic/" + \
            str(postid)
        return requests.post("https://scratch.mit.edu/discuss/subscription/topic/"+str(postid)+"/add/", headers=self.headers)

    def checkUserExists(self, user):
        return requests.get("https://api.scratch.mit.edu/accounts/checkusername/"+str(user)).json() == {"username": user, "msg": "username exists"}

    def getUserMessagesCount(self, user):
        self.headers['referer'] = "https://scratch.mit.edu"
        return requests.get("https://api.scratch.mit.edu/users/"+str(user)+"/messages/count").json()['count']

    def getMessages(self):
        print("https://api.scratch.mit.edu/users/" +
              str(self.username)+"messages" + "/")
        return requests.get("https://api.scratch.mit.edu/users/"+str(self.username)+"/messages" + "/", headers=self.headers).json()

    def getUserStatus(self, user):
        return requests.get("https://api.scratch.mit.edu/users/"+str(user)).json()['profile']['status']

    def getUserBio(self, user):
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
            logging.info('Re-sending the data')
            sendPacket({
                'method': 'set',
                'name': '☁ ' + variable,
                'value': str(value),
                'user': self.username,
                'project_id': str(PROJECT_ID)
            })
            time.sleep(0.1)

    def readCloudVar(self, name, limit="1000"):
        try:
            resp = requests.get("https://clouddata.scratch.mit.edu/logs?projectid=" +
                            str(PROJECT_ID)+"&limit="+str(limit)+"&offset=0").json()
            for i in resp:
                x = i['name']
                if x == ('☁ ' + str(name)):
                    return i['value']
        except:
            return 'Sorry, there was an error.'

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
        time.sleep(1.5)

    
    def turbowarpConnect(self, pid):
        global ws
        global PROJECT_ID
        PROJECT_ID = pid
        ws.connect('wss://clouddata.turbowarp.org',
               origin='https://turbowarp.org', enable_multithread=True)
        sendPacket({
            'method': 'handshake',
            'user': self.username,
            'project_id': str(pid)
        })
        time.sleep(1.5)


    def setTurbowarpVar(self, variable, value):
        sendPacket({
            'method': 'set',
            'name': '☁ ' + variable,
            'value': str(value),
            'user': self.username,
            'project_id': str(PROJECT_ID)
        })
        time.sleep(0.1)

def sendPacket(packet):
    ws.send(json.dumps(packet) + '\n')
