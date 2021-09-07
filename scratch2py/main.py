import requests
import re
import os
import websocket
import json
import time
import logging
import sys
import json
import ScratchEncoder
import os
try:
    ws = websocket.WebSocket()
except TypeError:
    logging.info('Tye y when prompted to reinstall websocket-client')
    os.system('pip uninstall websocket-client')
    os.system('pip install websocket-client')
encoder = ScratchEncoder.Encoder()

class Scratch2Py():
    def __init__(self, username, password):
        self.username = username
        # This is never used anywhere else...
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
    
    class project:
        def __init__(self, id):
            self.id = id

        def getStats(self, stat):
            if stat == "loves" or stat == "faves" or stat == "views" or stat == "remixes":
                if stat == "loves":
                    r = requests.get(
                        "https://api.scratch.mit.edu/projects/"+str(self.id))
                    data = r.json()
                    return data['stats']['loves']
                else:
                    if stat == "faves":
                        r = requests.get(
                            "https://api.scratch.mit.edu/projects/"+str(self.id))
                        data = r.json()
                        return data['stats']['favorites']
                    else:
                        if stat == "remixes":
                            r = requests.get(
                                "https://api.scratch.mit.edu/projects/"+str(self.id))
                            data = r.json()
                            return data['stats']['remixes']
                        else:
                            if stat == "views":
                                r = requests.get(
                                    "https://api.scratch.mit.edu/projects/"+str(self.id))
                                data = r.json()
                                return data['stats']['views']
        
        def getComments(self):
            uname = requests.get(
                "https://api.scratch.mit.edu/projects/"+str(self.id)).json()
            if uname != {"code": "NotFound", "message": ""}:
                uname = uname['author']['username']
                data = requests.get("https://api.scratch.mit.edu/users/" +
                                    str(uname)+"/projects/"+str(self.id)+"/comments").json()
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

        def getInfo(self):
            r = requests.get(
                'https://api.scratch.mit.edu/projects/'+str(self.id)
            ).json()
            return r

        def fetchAssets(self, type='img'):
            '''
            You may have problems with fetching assets since some projects may not have any assets, or are fetched as binary code and not JSON
            '''

            r = json.loads(requests.get(
                'https://projects.scratch.mit.edu/'+str(self.id)
            ).text.encode('utf-8'))
            
            assets = []
            for i in range(len(r['targets'])):
                if type == 'img':
                    assets.append('https://cdn.assets.scratch.mit.edu/internalapi/asset/'+str(r['targets'][i]['costumes'][0]['md5ext'])+'/get')
                elif type == 'snd':
                    assets.append('https://cdn.assets.scratch.mit.edu/internalapi/asset/'+str(r['targets'][i]['sounds'][0]['md5ext'])+'/get')
            return assets

    class studioSession:
        def __init__(self, sid):
            self.headers = {
            "x-csrftoken": "a",
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
            "referer": "https://scratch.mit.edu",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
            }
            self.sid = sid

        def inviteCurator(self, user):
            self.headers["referer"] = (
                "https://scratch.mit.edu/studios/" + str(self.sid) + "/curators/")
            requests.put("https://scratch.mit.edu/site-api/users/curators-in/" +
                        str(self.sid) + "/invite_curator/?usernames=" + user, headers=self.headers)

        def addStudioProject(self, pid):
            self.headers['referer'] = "https://scratch.mit.edu/projects/"+str(pid)
            return requests.post("https://api.scratch.mit.edu/studios/"+str(self.sid)+"/project/"+str(pid), headers=self.headers)

        def postComment(self, content, parent_id="", commentee_id=""):
            self.headers['referer'] = (
                "https://scratch.mit.edu/studios/" + str(self.sid) + "/comments/"
            )
            data = {
                "commentee_id": commentee_id,
                "content": content,
                "parent_id": parent_id,
            }
            return requests.post(
                "https://scratch.mit.edu/site-api/comments/gallery/"
                + str(self.sid)
                + "/add/",
                headers=self.headers,
                data=json.dumps(data),
            )

        def getComments(self):
            r = requests.get(
                "https://api.scratch.mit.edu/studios/"+str(self.sid)+"/comments")
            data = r.json()
            comments = []
            for i in data:
                x = i['content']
                comments.append(x)
            return json.dumps(comments)

        def follow(self):
            self.headers['referer'] = "https://scratch.mit.edu/studios/"+str(self.sid)
            return requests.put(
                "https://scratch.mit.edu/site-api/users/bookmarkers/"
                + str(self.sid)
                + "/remove/?usernames="
                + self.username,
                headers=self.headers,
            ).json()

        def unfollow(self):
            self.headers['referer'] = "https://scratch.mit.edu/studios/"+str(self.sid)
            return requests.put(
                "https://scratch.mit.edu/site-api/users/bookmarkers/"
                + str(id)
                + "/remove/?usernames="
                + self.username,
                headers=self.headers,
            ).json()

    class projectSession:
        def __init__(self, pid):
            self.headers = {
            "x-csrftoken": "a",
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
            "referer": "https://scratch.mit.edu",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
            }
            self.pid = pid

        def share(self):
            self.headers["referer"] = (
                "https://scratch.mit.edu/projects/"+str(self.pid)
            )
            return requests.put("https://api.scratch.mit.edu/proxy/projects/"+str(self.pid)+"/share",headers=self.headers)
        
        def unshare(self):
            self.headers["referer"] = (
                "https://scratch.mit.edu/projects/"+str(self.pid)
            )
            return requests.put("https://api.scratch.mit.edu/proxy/projects/"+str(self.pid)+"/unshare",headers=self.headers)

        def favorite(self):
            self.headers['referer'] = "https://scratch.mit.edu/projects/"+str(self.pid)
            return requests.post(
                "https://api.scratch.mit.edu/proxy/projects/"
                + str(self.pid)
                + "/favorites/user/"
                + self.username,
                headers=self.headers,
            ).json()

        def unfavorite(self):
            self.headers['referer'] = "https://scratch.mit.edu/projects/"+str(self.pid)
            return requests.delete(
                "https://api.scratch.mit.edu/proxy/projects/"
                + str(self.pid)
                + "/favorites/user/"
                + self.username,
                headers=self.headers,
            ).json()

        def love(self):
            self.headers['referer'] = "https://scratch.mit.edu/projects/"+str(self.pid)
            return requests.post(
                "https://api.scratch.mit.edu/proxy/projects/"
                + str(self.pid)
                + "/loves/user/"
                + self.username,
                headers=self.headers,
            ).json()

        def unlove(self):
            self.headers['referer'] = "https://scratch.mit.edu/projects/"+str(self.pid)
            return requests.delete(
                "https://api.scratch.mit.edu/proxy/projects/"
                + str(self.pid)
                + "/loves/user/"
                + self.username,
                headers=self.headers,
            ).json()

    class userSession:
        def __init__(self, username):
            self.headers = {
            "x-csrftoken": "a",
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
            "referer": "https://scratch.mit.edu",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
            }
            self.username = username

        def followUser(self, username):
            self.headers['referer'] = "https://scratch.mit.edu/users/" + \
                str(self.username)+"/"
            return requests.put(
                "https://scratch.mit.edu/site-api/users/followers/"
                + self.username
                + "/add/?usernames="
                + username,
                headers=self.headers,
            ).json()

        def unfollowUser(self, username):
            self.headers['referer'] = "https://scratch.mit.edu/users/" + \
                str(self.username)+"/"
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

    class user:
        def __init__(self, user):
            self.user = user
            self.headers = {
            "x-csrftoken": "a",
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
            "referer": "https://scratch.mit.edu",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
            }

        def exists(self):
            return requests.get("https://api.scratch.mit.edu/accounts/checkusername/"+str(self.user)).json() == {"username": self.user, "msg": "username exists"}

        def getMessagesCount(self):
            self.headers['referer'] = "https://scratch.mit.edu"
            return requests.get("https://api.scratch.mit.edu/users/"+str(self.user)+"/messages/count").json()['count']

        def getMessages(self):
            print("https://api.scratch.mit.edu/users/" +
                str(self.user)+"messages" + "/")
            return requests.get("https://api.scratch.mit.edu/users/"+str(self.user)+"/messages" + "/", headers=self.headers).json()

        def getStatus(self):
            return requests.get("https://api.scratch.mit.edu/users/"+str(self.user)).json()['profile']['status']

        def getBio(self):
            return requests.get("https://api.scratch.mit.edu/users/"+str(self.user)).json()['profile']['bio']

        def getProjects(self):
            r = requests.get(
                "https://api.scratch.mit.edu/users/"+str(self.user)+"/projects")
            data = r.json()
            titles = []
            for i in data:
                x = i['title']
                y = i['id']
                titles.append('ID: ' + str(y))
                titles.append('Title: ' + str(x))
            return titles

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
