from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import date
import pandas as pd
from time import sleep
import os
import random

from unfollowery.__cfg import get_driver


class Profile:
    """
    UnfollowersBot class is for getting usernames of unfollowers.
    * Unfollowers - The people, who has unfollowed the user.

    Args:
        username (str): The user's username string
        password (str): The user's password string
        sleep_time (float): Desired waiting time between
                            most of the Chromedriver actions
                            Recommended value: 5.0
                            (to not get caught by Instagram's algorithm)
        logs (bool): If True displays Selenium Chromedriver logs

    Attributes:
        username (str): The user's username
        password (str): The user's password
        sleep (float): Waiting time between most of the Chromedriver actions
                       (defined by the user or by default)

    Methods:
        followers (list): The list of the user's current Instagram followers
                          (and updates related CSV file)
        unfollowers (lst): The list of user's latest Instagram unfollowers
                           (and updates related CSV file)
        unfollowery (dict): Dictionary of the unfollowers based on
                            datetime arguments taken (if none, then returns
                            all time unfollowers)
    """

    def __init__(self,
                 username: str,
                 password: str,
                 sleep_time: float = 5.0,
                 logs: bool = False):
        """[Unfollowery class constructor].

        Params:
            username (str):
                The user's username
            password (str):
                The user's password
            sleep_time (float):
                Seconds to wait between most of the actions
                (to not get caught by Instagram's algorithm)
        """
        self.username = username
        self.password = password
        self.sleep = sleep_time
        self.__logs = logs

    @staticmethod
    def __scrolls(follower_count: int) -> int:
        """[Private]
        Number of times to scroll while in the Followers pop-up window
        to get to the bottom of the list.

        Params:
            follower_count (int): Amount of the user's Instagram followers

        Returns:
            int: The number of the needed scrolls
        """
        return int(follower_count) // 3

    @staticmethod
    def __sleep_random(sleep_time: float) -> float:
        """[Private]
        Change the waiting time (sleep_time) a little bit on each use
        to make it a little random and hard to be caught
        by Instagram's algorithm.

        Params:
            sleep_time (float): Waiting time in seconds
                                which will be randomized

        Returns:
            float: A little bit changed and randomized sleep_time time
        """
        return round(sleep_time * round(random.uniform(1, 1.4), 1), 1)

    @staticmethod
    def __datetime_form(datekey: str = None) -> str:
        """[Private]
        Get formatted datetime
        (current one, if "datekey" is None).

        Params:
            datekey (str): yyyymmdd formatted date

        Returns:
             str: Formatted date
        """
        if type(datekey) == int:
            datekey = str(datekey)

        if datekey is None:
            return date.today().strftime('%d-%m-%Y')
        elif datekey and len(datekey) == 12:
            return f'{datekey[-2:]}-{datekey[4:-2]}-{datekey[:4]}'
        else:
            error = '\nInvalid argument(s) for "datekey" parameter'
            dt_hint = '\n"datekey" format should be 8 char str - yyyymmdd'

            raise ValueError(error + dt_hint)

    def __login(self) -> webdriver.Chrome:
        """[Private]
        The login method authenticates the user with Instagram.

        [No arguments]

        Returns:
            webdriver.Chrome: Chromedriver object
        """

        # Log in...
        driver = get_driver(self.__logs)

        driver.get('https://www.instagram.com/accounts/login/')
        sleep(self.__sleep_random(self.sleep))

        # Find the Username box, make it empty and enter the username
        elem = driver.find_element(by=By.NAME, value='username')
        elem.clear()
        elem.send_keys(self.username)
        sleep(0.5)

        # Find the Password box, make it empty and enter the password
        elem = driver.find_element(by=By.NAME, value='password')
        elem.clear()
        elem.send_keys(self.password)
        sleep(0.5)

        elem.send_keys(Keys.RETURN)  # Submit
        sleep(0.5)

        return driver

    def followers(self) -> list:
        """Get the list of the user's current Instagram followers.

        [No params]

        Returns:
            list: The list of the user's followers
        """
        try:
            driver = self.__login()

            sleep(self.__sleep_random(self.sleep))
        except Exception as e:
            print('Unexpected problem with the login process...')
            raise e

        driver.get(f'https://www.instagram.com/{self.username}/')
        sleep(self.__sleep_random(self.sleep))

        # Find the follower count
        flwer_x = '//section/ul/li[2]/a/span'
        count_flwr = driver.find_element(by=By.XPATH, value=flwer_x)
        count_flwr = count_flwr.get_attribute('title')

        # Number of scrolls in the Followers pop-up window
        scr_times = self.__scrolls(count_flwr)
        sleep(self.__sleep_random(self.sleep))

        # Locate and scroll the followers mini-window
        view_followers = '//section/main/div/header/section/ul/li[2]/a'
        sleep(self.__sleep_random(self.sleep))

        driver.find_element(by=By.XPATH, value=view_followers).click()
        sleep(self.__sleep_random(self.sleep))

        fbody = driver.find_element(by=By.XPATH, value="//div[@class='isgrP']")
        scroll = 0

        # Loop for scrolling
        while scroll < scr_times:
            scrpt = """arguments[0].scrollTop = arguments[0].scrollTop
                                                + arguments[0].offsetHeight;"""
            driver.execute_script(scrpt, fbody)
            sleep(self.__sleep_random(1.5))
            scroll += 1

        # Get a list of all the (Followers') usernames
        # Find relevant hrefs
        inview_hrefs = driver.find_elements(by=By.TAG_NAME, value='a')
        inview_hrefs = [elem.get_attribute('title') for elem in inview_hrefs]
        f_list = []
        [f_list.append(title) for title in inview_hrefs if title not in f_list]

        # Remove first element, since it will always be ''
        del f_list[0]

        ig_profiles = []
        for username in f_list:
            ig_profiles.append(f'https://www.instagram.com/{username}/')

        df = pd.DataFrame({
            'Username': f_list,
            'IGProfile': ig_profiles
        })
        df.to_csv('latest_followers.csv', index=False)

        # Create (for future uses) "unfollowery.csv" file if it doesn't exists
        unfollowery_file = os.path.join(
            os.path.abspath(os.getcwd()), 'unfollowery.csv')
        if not os.path.exists(unfollowery_file):
            unfollowery_template = pd.DataFrame({
                'Username': [],
                'IGProfile': [],
                'Checked': []
            })

            unfollowery_template.to_csv(unfollowery_file)

        driver.close()

        return f_list

    def unfollowers(self) -> list:
        """This method gets difference between old and new follower lists.
        This difference contains unfollower usernames.

        [No params]

        Returns:
            list: Unfollowers list
        """
        today = self.__datetime_form()

        # Read the "latest_followers.csv" file.
        previous_followers_file = os.path.join(
            os.path.abspath(os.getcwd()), 'latest_followers.csv')
        old_followers = pd.read_csv(previous_followers_file)
        old_followers = set(old_followers['Username'].values.tolist())

        newf_set = set(self.followers())

        # Get the usernames of people who no longer follow the user
        # and convert it to a list to make a DataFrame
        unfollowers = old_followers.difference(newf_set)

        ig_profiles = []
        for username in list(unfollowers):
            ig_profiles.append(f'https://www.instagram.com/{username}/')

        df = pd.DataFrame({
            'Username': list(unfollowers),
            'IGProfile': ig_profiles,
            'Checked': today
        })

        # Append the DataFrame to "unfollowery.csv"
        unfollowery_file = os.path.join(
            os.path.abspath(os.getcwd()), 'unfollowery.csv')
        df.to_csv(unfollowery_file, mode='a', header=False, index=False)

        return list(unfollowers)

    def unfollowery(self, datekey: str = None,) -> dict:
        """Get unfollowers for specified (checked) date.
        If no args given, returns all time unfollowers.

        Params:
            datekey (str):datekey (str): yyyymmdd formatted date

        Returns:
             dict: dictionary[date] = list of unfollowers checked on date
        """
        unfollowery_file = os.path.join(
            os.path.abspath(os.getcwd()), 'unfollowery.csv')
        if not os.path.exists(unfollowery_file):
            raise FileNotFoundError('Could not find "unfollowers.csv"')

        unfollowers = pd.read_csv(unfollowery_file)
        unfollowery = {}

        # Get all time data (unfollowers)
        if datekey is None:
            dt_available = unfollowers.Checked.unique()

            for dt_value in dt_available:
                filtered = unfollowers.loc[unfollowers['Checked'] == dt_value]
                unfollowery[dt_value] = filtered['Username'].values.tolist()

            if bool(unfollowery):
                print(f'File "unfollowery.csv" is empty...')
                return
        # Get only unfollowers, that were checked on "dt"
        else:
            dt = self.__datetime_form(datekey=datekey)

            filtered = unfollowers.loc[unfollowers['Checked'] == dt]

            if filtered.empty:
                print(f'Could not find any data with the check date: {dt}')
                return

            unfollowery[dt] = filtered['Username'].values.tolist()

        return unfollowery
