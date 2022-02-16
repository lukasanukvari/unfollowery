# Unfollowery

For generating Instagram followers/unfollowers of the user in a list & file (without using Instagram API)

## Install

`pip install unfollowery`

## Usage

### Examples

Import the package and create `Profile` class instance:

```python
from unfollowery import Profile


# Obviously change USERNAME and
# PASSWORD with the real ones...
user = Profile(username='USERNAME', password='PASSWORD')
```

- Get the list of current followers:

```python
followers = user.unfollowers()
```

- Get the list of unfollowers since the last check:

```python
unfollowers = user.unfollowers()
```

- Get _dict_ ({[DATE]: [list(USERNAMES)]}) of all time unfollowers since the first check:

```python
all_time_unfollowers = user.unfollowery()
```

- Get unfollowers _dict_ ({[DATE]: [list(USERNAMES)}) from the specific date check:

```python
unfollowers_by_date = user.unfollowery(datekey='yyyymmdd')
```

_RECOMMENDED: Place your Instagram USERNAME and PASSWORD in the file (probably JSON) somewhere else and import it into your working file to not get displayed in the text editor._

### Class: `Profile`

Please see [Examples](#Examples) for initializing Instagram user's `unfollowery.Profile` class object.

#### Parameters:

- `username` _(str)_ : User's Instagram username
- `password` _(str)_ : User's Instagram password
- `sleep_time` _(float) - optional_ : Adjust waiting time (seconds) between some of the actions. It will still get randomized (_~sleep_time_). _Default value = 5_
- `logs` _(bool) - optional_ : If set to True, _Selenium_ and _Chromedriver_ logs will be displayed in the terminal. _Default value = False_

### Methods: `followers()` VS `unfollowers()`

The method `unfollowers()` **WILL NOT** return any usernames if `last_followers.csv` file does not exists.
If it exists `unfollowers()` will compare the usernames from `last_followers.csv` to the current followers, updates (appends) `unfollowery.csv` and updates (overwrites) `last_followers.csv`.

However, `followers()` **WILL ALWAYS** return the list of the current Instagram followers.

Either one of them will create **(IF THE FILES DO NOT EXIST)** both `last_followers.csv` - the list of the current followers and `unfollowery.csv` - the empty file to be filled (in the future) with the users that have unfollowed you.

_NOTE: The more followers the user has, the more time `followers()` and `unfollowers()` methods take to work._

### Method: `unfollowery()`

This method is for getting a _dict `{[DATE]: [list(USERNAMES)}`_ object which contains all time (since the first check) unfollowers.
However, one can give it a date `yyyymmdd` argument as written above in the [Examples](#-Examples) section.

### Keep in Mind

These methods may fail due to the updates on Instagram’s website, since it is crawler-based _(Selenium)_ package, so if you encounter any problems, please open an issue or contact me.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
