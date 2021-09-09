# Scratch2py

Scratch2py or S2py is a easy to use, versatile tool to communicate with the Scratch API
Based of [scratchclient](https://github.com/CubeyTheCube/scratchclient) by [Raihan142857](https://scratch.mit.edu/users/Raihan142857/)

## Installation

Run this command in your terminal as ONE command.

```bash
pip install scratch2py && pip uninstall websocket-client & pip install websocket-client
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
# Checks if a user exists. Returns true or false
user.getMessagesCount()
# Gets the number of messages someone has.
user.getMessages()
# Gets your messages and returns the JSON.
user.getStatus()
# Gets the 'about me' section of a users.
user.getBio()
# Gets the 'What I'm Working On' section of a users profile.
user.getProjects()
# Gets the projects that a user has.
```

## userSession class
```python
user = s2py.userSession('username')

user.followUser('otheruser')
# Follows a user
user.unfollowUser('thatotheruser')
# Unfollows a user
user.toggleCommenting()
# Toggles commenting on your profile (On/Off)
```

## studioSession class
```python
studio = s2py.studioSession('sid')

studio.inviteCurator('person')
# Invites a curator to a studio
studio.addStudioProject('pid')
# Adds a project to a studio
studio.postComment('Text', 'parentid', 'commentee_id')

studio.getComments()
# Gets the comments from a studio
studio.follow()
# Follows a studio
studio.unfollow()
# Unfollows a studio
```

## project class
```python
project = s2py.project('id')

project.getStats('loves/faves/remixes/views')
# Gets the stats of a project
project.getComments()
# Gets the comments of a project
project.getInfo()
# Gets the info of a project
```

## projectSession class

```python
project = s2py.projectSession('id')
# Starts a project session to the specific project

project.share()
# Shares a project
project.unshare()
# Unshares a project
project.favorite()
# Favorites a project
project.unfavorite()
# Unfavorites a project
project.love()
# Loves a project
project.unlove()
# Unloves a project
```

## cloud Class
Using the module for cloud.

```python
cloudproject = s2py.cloud('Project ID')
# Starts a cloud connection to a specific project
cloudproject.setCloudVar('CloudVar', 'Value')
# Sets a value to a cloud variable. Don't add the cloud symbol.
cloudproject.readCloudVar('variable name', 'Limit(optional)')
# Gets the value of a cloud variable. Limit is when the program should stop looking for the value. Limit is 1000 by default.
```

## Turbowarp and encode/decode functions

```python
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
=======
# Scratch2py

Scratch2py or S2py is a easy to use, versatile tool to communicate with the Scratch API
Based of [scratchclient](https://github.com/CubeyTheCube/scratchclient) by [Raihan142857](https://scratch.mit.edu/users/Raihan142857/)

## Installation

This command differs by system:

- Windows : `py -m pip install -r requirements.txt`
- Linux/Mac : `pip3 install -r requirements.txt`

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
# Checks if a user exists. Returns true or false
user.getMessagesCount()
# Gets the number of messages someone has.
user.getMessages()
# Gets your messages and returns the JSON.
user.getStatus()
# Gets the 'about me' section of a users.
user.getBio()
# Gets the 'What I'm Working On' section of a users profile.
user.getProjects()
# Gets the projects that a user has.
```

## userSession class
```python
user = s2py.userSession('username')

user.followUser('otheruser')
# Follows a user
user.unfollowUser('thatotheruser')
# Unfollows a user
user.toggleCommenting()
# Toggles commenting on your profile (On/Off)
```

## studioSession class
```python
studio = s2py.studioSession('sid')

studio.inviteCurator('person')
# Invites a curator to a studio
studio.addStudioProject('pid')
# Adds a project to a studio
studio.postComment('Text', 'parentid', 'commentee_id')

studio.getComments()
# Gets the comments from a studio
studio.follow()
# Follows a studio
studio.unfollow()
# Unfollows a studio
```

## project class
```python
project = s2py.project('id')

project.getStats('loves/faves/remixes/views')
# Gets the stats of a project
project.getComments()
# Gets the comments of a project
project.getInfo()
# Gets the info of a project
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

## Cloud class
Using the module for cloud.

```python
cloud = s2py.cloud('projectid')
cloud.setCloudVar('CloudVar', 'Value')
# Sets a value to a cloud variable. Don't add the cloud symbol.
cloud.readCloudVar('variable name', 'Limit(optional)')
# Gets the value of a cloud variable. Limit is when the program should stop looking for the value. Limit is 1000 by default.
cloud.encode('value')
# Encodes a value. Scratch version available on my Scratch profile
cloud.decode('value')
# Decodes a value. To be used to communicate to and from a Scratch project.
cloud.turbowarpConnect('pid')
# Connects to a turbowarp project
cloud.setTurbowarpVar('var','value')
# Changes the value of a turbowarp var.
```
## The End

That's it!
Contact my on my [Scratch profile](https://scratch.mit.edu/users/TheCloudDev/#comments)

