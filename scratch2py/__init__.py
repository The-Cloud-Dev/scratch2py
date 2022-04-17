'''
Scratch2py or s2py is an easy-to-use, versatile tool to communicate with the Scratch API and do other things
   >>> from scratch2py import Scratch2Py
   >>> s2py = Scratch2Py('foobar', 'spameggs')
   >>> user = s2py.user('Scratchteam')
   >>> user.exists()
   True
'''

from wsgiref import headers
import websocket
import requests
import logging
import json
import re

ws = websocket.WebSocket()


class Scratch2Py():
    '''Initialize a new Scratch2Py object'''

    def __init__(self, username: str, password: str) -> None:
        self.chars = """AabBCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789 -_`~!@#$%^&*()+=[];:'"\|,.<>/?}{"""
        global uname
        uname = username
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
            global sessionId
            sessionId = self.sessionId
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
            raise Exception(
                'Error: Invalid credentials. Authentication failed.')
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
        '''Encode a value.'''
        decoded = ""
        text = str(text)
        y = 0
        for i in range(0, len(text)//2):
            x = self.chars[int(str(text[y])+str(text[int(y)+1]))-1]
            decoded = str(decoded)+str(x)
            y += 2
        return decoded

    def encode(self, text):
        '''Decode a value.'''
        encoded = ""
        length = int(len(text))
        for i in range(0, length):
            try:
                x = int(self.chars.index(text[i])+1)
                if x < 10:
                    x = str(0)+str(x)
                encoded = encoded + str(x)
            except ValueError:
                logging.error('Character not supported')
        return encoded

    class project:
        '''Get project related information'''

        def __init__(self, id: int) -> None:
            self.id = id

        def getStats(self) -> dict:
            '''Fetch statistics for a project'''
            r = requests.get(
                "https://api.scratch.mit.edu/projects/"+str(self.id))
            data = r.json()
            return data['stats']

        def getComments(self) -> 'list[dict]':
            '''Fetch comments for a project'''
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
                        comments.append(
                            str('Username: '+str(uname))+(str(', Content: ')+str(x)))
                    return data

        def getInfo(self) -> dict:
            '''Fetch the entire project information'''
            r = requests.get(
                'https://api.scratch.mit.edu/projects/'+str(self.id)
            ).json()
            return r

        def getAssets(self, type='img') -> 'list[str]':
            '''
            Fetch project asset URLs such as their costumes and sounds
            You may have problems with fetching assets since some projects may not have any assets, or are fetched as binary code and not JSON
            '''

            r = json.loads(requests.get(
                'https://projects.scratch.mit.edu/'+str(self.id)
            ).text.encode('utf-8'))

            assets = []
            for i in range(len(r['targets'])):
                if type == 'img':
                    assets.append('https://cdn.assets.scratch.mit.edu/internalapi/asset/' +
                                  str(r['targets'][i]['costumes'][0]['md5ext'])+'/get')
                elif type == 'snd':
                    assets.append('https://cdn.assets.scratch.mit.edu/internalapi/asset/' +
                                  str(r['targets'][i]['sounds'][0]['md5ext'])+'/get')
            return assets

    class studioSession:
        '''Get studio related information'''

        def __init__(self, sid: int) -> None:
            self.headers = {
                "x-csrftoken": "a",
                "x-requested-with": "XMLHttpRequest",
                "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
                "referer": "https://scratch.mit.edu",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
            }
            self.sid = sid

        def inviteCurator(self, user: str) -> None:
            '''Invite a curator to a studio'''
            self.headers["referer"] = (
                "https://scratch.mit.edu/studios/" + str(self.sid) + "/curators/")
            requests.put("https://scratch.mit.edu/site-api/users/curators-in/" +
                         str(self.sid) + "/invite_curator/?usernames=" + user, headers=self.headers)

        def addStudioProject(self, pid: int):
            '''Add a project to a studio'''
            self.headers['referer'] = "https://scratch.mit.edu/projects/" + \
                str(pid)
            return requests.post("https://api.scratch.mit.edu/studios/"+str(self.sid)+"/project/"+str(pid), headers=self.headers)

        def postComment(self, content: str, parent_id: str = "", commentee_id: str = ""):
            '''Post a comment on a studio'''
            self.headers['referer'] = (
                "https://scratch.mit.edu/studios/" +
                str(self.sid) + "/comments/"
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

        def getComments(self) -> 'list[str]':
            '''Fetch studio comments'''
            r = requests.get(
                "https://api.scratch.mit.edu/studios/"+str(self.sid)+"/comments")
            data = r.json()
            comments = []
            for i in data:
                x = i['content']
                comments.append(x)
            return comments

        def follow(self) -> dict:
            '''Follow a studio'''
            self.headers['referer'] = "https://scratch.mit.edu/studios/" + \
                str(self.sid)
            return requests.put(
                "https://scratch.mit.edu/site-api/users/bookmarkers/"
                + str(self.sid)
                + "/remove/?usernames="
                + self.username,
                headers=self.headers,
            ).json()

        def unfollow(self) -> dict:
            '''Unfollow a studio'''
            self.headers['referer'] = "https://scratch.mit.edu/studios/" + \
                str(self.sid)
            return requests.put(
                "https://scratch.mit.edu/site-api/users/bookmarkers/"
                + str(id)
                + "/remove/?usernames="
                + self.username,
                headers=self.headers,
            ).json()

    class projectSession:
        '''Do project related things as a "user"'''

        def __init__(self, pid: int) -> None:
            self.headers = {
                "x-csrftoken": "a",
                "x-requested-with": "XMLHttpRequest",
                "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
                "referer": "https://scratch.mit.edu",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
            }
            self.pid = pid

        def share(self):
            '''Share a project'''
            self.headers["referer"] = (
                "https://scratch.mit.edu/projects/"+str(self.pid)
            )
            return requests.put("https://api.scratch.mit.edu/proxy/projects/"+str(self.pid)+"/share", headers=self.headers)

        def unshare(self):
            '''Unshare a project'''
            self.headers["referer"] = (
                "https://scratch.mit.edu/projects/"+str(self.pid)
            )
            return requests.put("https://api.scratch.mit.edu/proxy/projects/"+str(self.pid)+"/unshare", headers=self.headers)

        def favorite(self):
            '''Favorite (star) a project'''
            self.headers['referer'] = "https://scratch.mit.edu/projects/" + \
                str(self.pid)
            return requests.post(
                "https://api.scratch.mit.edu/proxy/projects/"
                + str(self.pid)
                + "/favorites/user/"
                + self.username,
                headers=self.headers,
            ).json()

        def unfavorite(self):
            '''Unfavorite (star) a project'''
            self.headers['referer'] = "https://scratch.mit.edu/projects/" + \
                str(self.pid)
            return requests.delete(
                "https://api.scratch.mit.edu/proxy/projects/"
                + str(self.pid)
                + "/favorites/user/"
                + self.username,
                headers=self.headers,
            ).json()

        def love(self):
            '''Love (heart) a project'''
            self.headers['referer'] = "https://scratch.mit.edu/projects/" + \
                str(self.pid)
            return requests.post(
                "https://api.scratch.mit.edu/proxy/projects/"
                + str(self.pid)
                + "/loves/user/"
                + self.username,
                headers=self.headers,
            ).json()

        def unlove(self):
            '''Unlove (heart) a project'''
            self.headers['referer'] = "https://scratch.mit.edu/projects/" + \
                str(self.pid)
            return requests.delete(
                "https://api.scratch.mit.edu/proxy/projects/"
                + str(self.pid)
                + "/loves/user/"
                + self.username,
                headers=self.headers,
            ).json()

        def remix(self):
            '''Remix a project'''
            self.headers['referer'] = "https://scratch.mit.edu/projects/" + \
                str(self.pid)
            return requests.post("https://projects.scratch.mit.edu/?is_remix=1&original_id="+str(self.pid)+"&title=Scratch%20Project").json()

    class userSession:
        '''Do profile related things as a "user"'''

        def __init__(self, username: str) -> None:
            self.headers = {
                "x-csrftoken": "a",
                "x-requested-with": "XMLHttpRequest",
                "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
                "referer": "https://scratch.mit.edu",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
            }
            self.username = uname
            self.uname2 = username

        def followUser(self):
            '''Follow a user'''
            self.headers['referer'] = "https://scratch.mit.edu/users/" + \
                str(self.username)+"/"
            return requests.put(
                "https://scratch.mit.edu/site-api/users/followers/"
                + self.username
                + "/add/?usernames="
                + self.uname2,
                headers=self.headers,
            ).json()

        def unfollowUser(self):
            '''Unfollow a user'''
            self.headers['referer'] = "https://scratch.mit.edu/users/" + \
                str(self.username)+"/"
            return requests.put(
                "https://scratch.mit.edu/site-api/users/followers/"
                + self.username
                + "/remove/?usernames="
                + self.uname2,
                headers=self.headers,
            ).json()

        def toggleCommenting(self):
            '''Toggle a user profile's comment section'''
            self.headers['referer'] = "https://scratch.mit.edu/users/" + \
                str(self.username)
            return requests.post(
                "https://scratch.mit.edu/site-api/comments/user/" +
                str(self.username)+"/toggle-comments/",
                headers=self.headers,
            )

        def postComment(self, content: str, parent_id: str = "", commentee_id: str = ""):
            '''Post a comment on a user profile'''
            self.headers['referer'] = "https://scratch.mit.edu/users/" + self.uname2
            data = {
                'content': content,
                'parent_id': parent_id,
                'commentee_id': commentee_id
            }
            return requests.post("https://scratch.mit.edu/site-api/comments/user/" + self.uname2 + "/add/", data=json.dumps(data), headers=self.headers).json()

    class user:
        '''Do profile related things'''

        def __init__(self, user: str) -> None:
            self.user = user
            self.headers = {
                "x-csrftoken": "a",
                "x-requested-with": "XMLHttpRequest",
                "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
                "referer": "https://scratch.mit.edu",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
            }

        def exists(self) -> bool:
            '''Check if a user exists. Returns true or false'''
            return requests.get("https://api.scratch.mit.edu/accounts/checkusername/"+str(self.user)).json() == {"username": self.user, "msg": "username exists"}

        def getMessagesCount(self):
            '''Get the number of messages someone posted'''
            self.headers['referer'] = "https://scratch.mit.edu"
            return requests.get("https://api.scratch.mit.edu/users/"+str(self.user)+"/messages/count", headers=self.headers).json()['count']

        def getMessages(self) -> dict:
            '''Get the messages someone sent'''
            return requests.get("https://api.scratch.mit.edu/users/"+str(self.user)+"/messages" + "/", headers=self.headers).json()

        def getStatus(self) -> str:
            '''Get the "About Me" section of a user profile'''
            return requests.get("https://api.scratch.mit.edu/users/"+str(self.user)).json()['profile']['status']

        def getBio(self) -> str:
            '''Get the 'What I'm Working On' section of a user profile'''
            return requests.get("https://api.scratch.mit.edu/users/"+str(self.user)).json()['profile']['bio']

        def getProjects(self) -> 'dict[str, list]':
            r = requests.get(
                "https://api.scratch.mit.edu/users/"+str(self.user)+"/projects")
            data = r.json()
            titles = {}
            for i in data:
                x = i['title']
                y = i['id']
                z = i['history']['shared']
                titles[x] = [y, z]
            return titles

    class scratchConnect:
        '''Connect to a project to read and write cloud variables'''

        def __init__(self, pid: int):
            global ws
            global PROJECT_ID
            self.username = uname
            PROJECT_ID = pid
            ws.connect('wss://clouddata.scratch.mit.edu', cookie='scratchsessionsid='+sessionId+';',
                       origin='https://scratch.mit.edu', enable_multithread=True)
            ws.send(json.dumps({
                'method': 'handshake',
                'user': self.username,
                'project_id': str(pid)
            }) + '\n')

        def setCloudVar(self, variable: str, value: str) -> None:
            '''Set the value of a cloud variable (☁ is not needed)'''
            try:
                ws.send(json.dumps({
                    'method': 'set',
                    'name': '☁ ' + variable,
                    'value': str(value),
                    'user': self.username,
                    'project_id': str(PROJECT_ID)
                }) + '\n')
            except BrokenPipeError:
                logging.error('Broken Pipe Error. Connection Lost.')
                ws.connect('wss://clouddata.scratch.mit.edu', cookie='scratchsessionsid='+sessionId+';',
                           origin='https://scratch.mit.edu', enable_multithread=True)
                ws.send(json.dumps({
                    'method': 'handshake',
                    'user': self.username,
                    'project_id': str(PROJECT_ID)
                }) + '\n')
                logging.info('Re-connected to wss://clouddata.scratch.mit.edu')
                logging.info('Re-sending the data')
                ws.send(json.dumps({
                    'method': 'set',
                    'name': '☁ ' + variable,
                    'value': str(value),
                    'user': self.username,
                    'project_id': str(PROJECT_ID)
                }) + '\n')

        def readCloudVar(self, name: str, limit: str = "1000") -> str:
            '''Read the value of a cloud variable (an exception may be raised if reading fails)'''
            try:
                resp = requests.get("https://clouddata.scratch.mit.edu/logs?projectid=" +
                                    str(PROJECT_ID)+"&limit="+str(limit)+"&offset=0").json()
                for i in resp:
                    x = i['name']
                    if x == ('☁ ' + str(name)):
                        return i['value']
            except Exception:
                raise Exception('Cloud variable could not be read.')

    class scratchDatabase:
        '''Create a new database that will detect messages on a certain project ID'''

        def __init__(self, pid: int) -> None:
            self.chars = """AabBCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789 -_`~!@#$%^&*()+=[];:'"\|,.<>/?}{"""
            self.id = pid
            self.username = uname
            ws.connect('wss://clouddata.scratch.mit.edu', cookie='scratchsessionsid='+sessionId+';',
                       origin='https://scratch.mit.edu', enable_multithread=True)
            ws.send(json.dumps({
                'method': 'handshake',
                'user': self.username,
                'project_id': str(self.id)
            }) + '\n')

        def __decode(self, text):
            decoded = ""
            text = str(text)
            y = 0
            for i in range(0, len(text)//2):
                x = self.chars[int(str(text[y])+str(text[int(y)+1]))-1]
                decoded = str(decoded)+str(x)
                y += 2
            return decoded

        def __encode(self, text):
            encoded = ""
            length = int(len(text))
            for i in range(0, length):
                try:
                    x = int(self.chars.index(text[i])+1)
                    if x < 10:
                        x = str(0)+str(x)
                    encoded = encoded + str(x)
                except ValueError:
                    logging.error('Character not supported')
            return encoded

        def __setCloudVar(self, variable, value):
            try:
                ws.send(json.dumps({
                    'method': 'set',
                    'name': '☁ ' + variable,
                    'value': str(value),
                    'user': self.username,
                    'project_id': str(self.id)
                }) + '\n')
            except BrokenPipeError:
                logging.error('Broken Pipe Error. Connection Lost.')
                ws.connect('wss://clouddata.scratch.mit.edu', cookie='scratchsessionsid='+sessionId+';',
                           origin='https://scratch.mit.edu', enable_multithread=True)
                ws.send(json.dumps({
                    'method': 'handshake',
                    'user': self.username,
                    'project_id': str(self.id)
                }) + '\n')
                logging.info('Re-connected to wss://clouddata.scratch.mit.edu')
                logging.info('Re-sending the data')
                ws.send(json.dumps({
                    'method': 'set',
                    'name': '☁ ' + variable,
                    'value': str(value),
                    'user': self.username,
                    'project_id': str(self.id)
                }) + '\n')

        def __readCloudVar(self, name, limit="1000"):
            try:
                resp = requests.get("https://clouddata.scratch.mit.edu/logs?projectid=" +
                                    str(self.id)+"&limit="+str(limit)+"&offset=0").json()
                for i in resp:
                    x = i['name']
                    if x == ('☁ ' + str(name)):
                        return i['value']
            except json.decoder.JSONDecodeError:
                resp = requests.get("https://clouddata.scratch.mit.edu/logs?projectid=" +
                                    str(self.id)+"&limit="+str(limit)+"&offset=0").json()
                for i in resp:
                    x = i['name']
                    if x == ('☁ ' + str(name)):
                        return i['value']

        def startLoop(self):
            '''Start a new loop for the database'''
            data = []
            while True:
                encodedMethod = self.__readCloudVar('Method')
                if encodedMethod != None:
                    Method = self.__decode(encodedMethod)
                if Method == "set":
                    encodedSend = self.__readCloudVar('Send')
                    Send = str(self.__decode(encodedSend))
                    encodedVal = self.__readCloudVar('Data')
                    Val = str(self.__decode(encodedVal))
                    intVal = self.__decode(encodedVal)
                    c = 0
                    for i in Send:
                        if str(i) in "1234567890":
                            c = int(c)+1
                    if c == len(Send):
                        if int(Send) > len(data):
                            if int(Send) == int(len(data))+1:
                                data.append(intVal)
                                logging.info('Data added.')
                                tosend = self.__encode('Data added.')
                                self.__setCloudVar('Return', tosend)
                                self.__setCloudVar('Method', '')
                            else:
                                while len(data) != int(Send)-1:
                                    data.append('none')
                                data.append(intVal)
                                logging.info('Data added.')
                                tosend = self.__encode('Data added.')
                                self.__setCloudVar('Return', tosend)
                                self.__setCloudVar('Method', '')
                        else:
                            data.pop(int(Send)-1)
                            data.insert(int(Send), intVal)
                            logging.info('Data added.')
                            tosend = self.__encode('Data added.')
                            self.__setCloudVar('Return', tosend)
                            self.__setCloudVar('Method', '')
                    else:
                        tosend = self.__encode(
                            'Invalid input. Variable name must be int.')
                        self.__setCloudVar('Return', tosend)
                if Method == "get":
                    encodedSend = self.__readCloudVar('Send')
                    Send = self.__decode(encodedSend)
                    c = 0
                    for i in Send:
                        if str(i) in "1234567890":
                            c = int(c)+1
                    if c == len(Send) and int(Send) > 0 and int(Send) < int(len(data))+1:
                        tosend = self.__encode(data[int(Send)-1])
                        self.__setCloudVar('Return', tosend)
                        logging.info('Data sent.')
                        self.__setCloudVar('Method', '')
                    else:
                        tosend = self.__encode('Invalid input.')
                        self.__setCloudVar('Return', tosend)
                if Method == "delete":
                    encodedSend = self.__readCloudVar('Send')
                    Send = self.__decode(encodedSend)
                    c = 0
                    for i in Send:
                        if str(i) in "1234567890":
                            c = int(c)+1
                    if c == len(Send) and int(Send) > 0 and int(Send) < int(len(data))+1:
                        data.pop(int(Send)-1)
                        data.insert(int(Send)-1, 'none')
                        logging.info('Variable deleted.')
                        tosend = self.__encode('Variable deleted.')
                        self.__setCloudVar('Return', tosend)
                    else:
                        tosend = self.__encode('Invalid input.')
                        self.__setCloudVar('Return', tosend)
