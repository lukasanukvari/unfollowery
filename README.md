# InstaUnfollowers

📷 Instagram bot for Windows 10:
- Get the list of the Instagram users that unfollowed you, without using Instagram API.

This bot may fail due to updates on Instagram’s website. If you encounter any problems, please contact me.

## Install
1. Make sure you have Chrome browser installed.
3. Install required packages: `pip3 install -r requirements.txt`
4. Replace json file values *USERNAMEHERE* and *PASSWORDHERE* in `client_secret.json` with the real ones..
```json
{
    "username": "USERNAMEHERE",
    "password": "PASSWORDHERE"
}
```

## Get Unfollowers
### How `bot.py` Works
The application WILL NOT return any unfollowers at its first run.  
It will create `last_followers.txt` - the list of the current followers and `unfollowers.txt` - the list of the users that unfollowed you.  
**NOTE:** *There will be no unfollowers at first in `unfollowers.txt`*  
Then, on each run, it compares the followers list to the current followers, updates (appends) `unfollowers.txt` and updates (overwrites) `last_followers.txt`

`./utils/config.py` sets Chrome to run in headless mode - running browser/driver in background without popping up (you may change it by changing *options.headless* value to *False*)
Current value is *True*:
```python
options.headless = True
```

### Usage
Change directory to **InstaUnfollowers**: Run `cd path/to/InstaUnfollowers`.
To run the program once (no scheduling), run `python main.py` in the command line or double-click on it.
Otherwise, if you wish the run to be scheduled every *N* hours run `python runscheduled.py`.

Set *N* value as you wish, for the moment its value is 1 (application will run every hour).
```python
# Schedule unfollowers check for every N hours
N = 1
```

If you would like to, you could automate running this script with Windows Task Scheduler too.
**NOTE:** *If you tend to use Windows Task Scheduler use `main.py` instead of `runscheduler.py`*  

### Scheduling a Python Script with Task Scheduler
To schedule a Python script with Task scheduler, create an action and add the path to your Python executable file, add the path to the script in the "Start in" box and add the name of the Python file as an argument. Then, create a trigger to schedule the execution of your script.

[DETAILED EXPLANATION](https://dev.to/abautista/automate-a-python-script-with-task-scheduler-3fb6)  
[VIDEO TUTORIAL](https://www.youtube.com/watch?v=n2Cr_YRQk7o)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
