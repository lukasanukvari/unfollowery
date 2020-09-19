# InstaUnfollowers

📷 Instagram bot for Windows 10:
- Get the list of the Instagram users that unfollowed you, without using Instagram API. `main_bot.py`
- Get Instagram stats (Posts/Followers/Following) of entered user (firstly, you will be asked to enter your login information). `stats_bot.py`

This bot may fail due to updates on Instagram’s website. If you encounter any problems, please contact me.

## Install
1. Make sure you have Chrome browser installed. Also, check your Chrome version from *chrome://version/*
2. Download [Chromedriver](https://chromedriver.chromium.org/downloads) and put it into utils folder: `./utils/chromedriver`
3. Install Selenium: `pip3 install -r requirements.txt`
4. Replace words *USERNAME* and *PASSWORD* in line 95 of `main_bot.py` with the real ones (program needs to log in to work properly).
```python
mainBot = SmarterBot('USERNAME', 'PASSWORD',)
```

## Get Unfollowers
### How `main_bot.py` Works
The program WILL NOT return any unfollowers at its first run.  
It will create `last_followers.py` - the list of the current followers and `unfollowers.txt` - the list of the users that unfollowed you.  
**NOTE:** *There will be no unfollowers at first in `unfollowers.txt`*  
Then, on each run, it compares the list to the current followers, updates (no overwriting, it appends) `unfollowers.txt` and updates (overwrites) `last_followers.txt`

`./utils/set_chrome.py` sets Chrome to run in headless mode - running browser/driver in background without popping up.

### Usage
Change directory to **InstaUnfollowers**.  
Run `python main_bot.py`

If you would like, you could automate running this script with Task Scheduler.

### Scheduling a Python Script with Task Scheduler
To schedule a Python script with Task scheduler, create an action and add the path to your Python executable file, add the path to the script in the "Start in" box and add the name of the Python file as an argument. Then, create a trigger to schedule the execution of your script.

[DETAILED EXPLANATION](https://dev.to/abautista/automate-a-python-script-with-task-scheduler-3fb6)  
[VIDEO TUTORIAL](https://www.youtube.com/watch?v=n2Cr_YRQk7o)

## Get Stats by Username

### Usage
`stats_bot.py` is a console application, so you can just change directory to **InstaUnfollowers** and run `python stats_bot.py`  
The program will ask to enter the Instagram username and password. Then it will log in and print user's own stats, then asks if he/she wants to get another user's stats and acts accordingly.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.