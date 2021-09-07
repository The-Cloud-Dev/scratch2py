# Scratch2py

Scratch2py or S2py is a easy to use, versatile tool to communicate with the Scratch API
Based of [scratchclient](https://github.com/CubeyTheCube/scratchclient) by [Raihan142857](https://scratch.mit.edu/users/Raihan142857/)

## Installation

Run this command in your terminal as ONE command.

```bash
pip install scratch2py && pip install --upgrade websocket-client
```

## Usage

Import scratch2py in like this:

```python
import scratch2py
s2py = scratch2py.Scratch2Py('username', 'password')
# Imports s2py and initializes a new s2py object. Enter your Scratch MIT credentials to create a connection with the API.
```

## user class
```python
user = s2py.user('username')

user.exists()
user.getMessagesCount()
user.getMessages()
user.getMessages()
user.getStatus()
user.getBio()
user.getProjects()
```

## userSession class
```python
user = s2py.userSession('username')

user.followUser('otheruser')
user.unfollowUser('thatotheruser')
user.toggleCommenting()
```

## studioSession class
```python
studio = s2py.studioSession('sid')

studio.inviteCurator('person')
studio.addStudioProject('pid')
studio.postComment('so cool', 'parentid', 'commentee_id')
studio.getComments()
studio.follow()
studio.unfollow()
```

## project class
```python
project = s2py.project('id')

project.getStats('loves/faves/remixes/views')
project.getComments()
project.getInfo()
```

## projectSession class
```
project = s2py.projectSession('id')

project.share()
project.unshare()
project.favorite()
project.unfavorite()
project.love()
project.unlove()
```

## Cloud
Using the module for cloud.

```python
s2py.cloudConnect('Project ID')
# Starts a cloud connection to a specific project
s2py.setCloudVar('CloudVar', 'Value')
# Sets a value to a cloud variable. Don't add the cloud symbol.
s2py.readCloudVar('variable name', 'Limit(optional)')
# Gets the value of a cloud variable. Limit is when the program should stop looking for the value. Limit is 1000 by default.
s2py.encode('value')
# Encodes a value. Scratch version available on my Scratch profile
s2py.decode('value')
# Decodes a value. To be used to communicate to and from a Scratch project.
s2py.turbowarpConnect('pid')
# Connects to a turbowarp project
s2py.setTurbowarpVar('var','value')
# Changes the value of a turbowarp var.
```
## The End

That's it!
Contact my on my [Scratch profile](https://scratch.mit.edu/users/TheCloudDev/#comments)
