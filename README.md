# Scratch2py

Scratch2py or S2py is a easy to use, versatile tool to communicate with the Scratch API
Based of [scratchclient](https://github.com/CubeyTheCube/scratchclient) by [Raihan142857](https://scratch.mit.edu/users/Raihan142857/)

## Installation

Use your terminal and run these command to install Scratch2py and websocket
Then, import the module into your python file like this:

```bash
pip install scratch2py
pip uninstall websocket-client
pip install websocket-client
```

```python
import scratch2py
s2py = scratch2py.s2py('username', 'password')
# Imports s2py and initializes a new s2py object. Enter your Scratch MIT credentials to create a connection with the API.
```

## Usage

How to use S2py

## Projects

Using the module for projects

```python
s2py.getStats('id', 'stat')
# Gets the stats of a project. First input is the project ID, the second one is what stat you want (Loves, faves, views or remixes)
s2py.getProjectComments('id')
# Gets the comments of a project based on the project ID. Data returned in JSON.
s2py.shareProject('pid')
# Shares a project based on the project ID.
s2py.unshareProject('pid')
# Unshares a projec based on the project ID.
```

## Studios

Using the module for a studio

```python
s2py.getStudioComments('id')
# Gets the comments of a studio based on the ID.
s2py.postStudioComments('studio id','content','parent id','commentee id')
# Posts a comment on a studio. (See s2py.postProjectComments for param ^)
s2py.followStudio('studio id')
# Follows a studio based on the ID.
s2py.unfollowStudio('Studio id')
# Unfollows a studio based on the ID.
s2py.inviteCurator('studio id','username')
# Invites someone to a studio.
```

## User

Using the module for getting user data

```python
s2py.getUserStatus('user')
# Gets the 'about me' section of a users.
s2py.getUserBio('user')
# Gets the 'What I'm Working On' section of a users profile.
s2py.getUserMessagesCount('user')
# Gets the number of messages someone has.
s2py.checkUserExists('user')
# Checks if a user exists. Returns true or false
s2py.love('project id')
# Loves a project based on the ID.
s2py.unlove('project id')
# Unloves a project based on the ID.
s2py.favorite('project id')
# Favorites a project based on the ID.
s2py.unfavorite('project id')
# Unfavorites a project based on the ID.
s2py.followUser('name')
# Follows a user based on the username.
s2py.unfollowUser('name')
# Unfollows a user based on the username.
s2py.toggleCommenting()
# Toggles comments for your profile.
s2py.getMessages()
# Gets your messages and returns the JSON.
```

## Forums

```python
s2py.followPost(postid)
# Follows a post based on the post ID.
s2py.unfollowPost(postid)
# Unfollows a post based on the post ID.
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
```

## The End

That's it!
Contact my on my [Scratch profile](https://scratch.mit.edu/users/TheCloudDev/#comments)
