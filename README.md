# Scratch2py

Scratch2py or S2py is a easy to use, versatile tool to communicate with the Scratch API
Based of [scratchclient](https://github.com/CubeyTheCube/scratchclient) by [Raihan142857](https://scratch.mit.edu/users/Raihan142857/)

## Installation

```bash
pip install scratch2py
```

Use your terminal and run this command to install Scratch2py
Then, import the module into your python file like this:

```python
import scratch2py
s2py = scratch2py.constructer('username', 'password')
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
```

## Studios

Using the module for a studio

```python
s2py.getStudioComments('id')
# Gets the comments of a studio based on the ID.
```

## User

Using the module for getting user data

```python
s2py.getUserStatus('user')
# Gets the 'about me' section of a users.
s2py.getUserBio('user')
# Gets the 'What I'm Working On' section of a users profile.
s2py.getUserFollowersCount('user')
# Gets the number of followers for a user
s2py.getUserMessagesCount('user')
# Gets the number of messages someone has.
s2py.checkUserExists('user')
# Checks if a user exists. Returns true or false
s2py.getProjects('user')
# Gets the titles and project IDs of a user.
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
```

## The End

That's it!
Contact my on my [Scratch profile](https://scratch.mit.edu/users/TheCloudDev/#comments)
