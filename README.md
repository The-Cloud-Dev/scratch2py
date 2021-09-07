# Scratch2py

Scratch2py or S2py is a easy to use, versatile tool to communicate with the Scratch API
Based of [scratchclient](https://github.com/CubeyTheCube/scratchclient) by [Raihan142857](https://scratch.mit.edu/users/Raihan142857/)

## Installation

Run this command in your terminal as ONE command.

```bash
pip install scratch2py && pip uninstall websocket-client && pip install websocket-client
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

## Cloud stuff?
Still there. It is in the main `s2py` class.

## The End

That's it!
Contact my on my [Scratch profile](https://scratch.mit.edu/users/TheCloudDev/#comments)
