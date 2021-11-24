from utils.config import driver, sleep_time
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from time import sleep
import os


class UnfollowersBot:
    """
    UnfollowersBot class is for getting usernames of unfollowers.

    * Unfollowers - The people, who has unfollowed the user.

    Attributes:
        login (void):
            Method for Instagram user authentication.
        followers (list):
            Get the list of the users's Instagram followers.
        file_work (void):
            Method for comparison of old and new followers' files.
        username (str):
            The user's username.
        password (str):
            The user's password.
        driver (Selenium.webdriver.Chrome):
            The driver of Chrome to automate its actions.
"""

    def __init__(self, username, password):
        """
        Arguments:
            username (str):
                The user's username.
            password (str):
                The user's password.
        """
        self.username = username
        self.password = password
        self.driver = driver

        # Log in...
        try:
            self.login()
            print('Successfully logged in!')
            sleep(sleep_time)
        except Exception as e:
            print('Unexpected problem with the login process...')
            raise e

        followers = self.followers()
        self.driver.close()

        self.file_work(followers)

    def login(self):
        """The login method authenticates the user with Instagram.

        [No arguments]
        """
        self.driver.get('https://www.instagram.com/accounts/login/')
        sleep(sleep_time)

        # Find the Username box, make it empty and enter the username
        elem = self.driver.find_element_by_name('username')
        elem.clear()
        elem.send_keys(self.username)

        # Find the Password box, make it empty and enter the password
        elem = self.driver.find_element_by_name('password')
        elem.clear()
        elem.send_keys(self.password)
        elem.send_keys(Keys.RETURN)  # Submit

    def followers(self):
        """Get the list of the users's Instagram followers.

        Returns:
            list: The list of user's followers.
        """
        self.driver.get(f'https://www.instagram.com/{self.username}/')
        sleep(sleep_time)

        # Find the number of followers.
        flwer_x = '//section/ul/li[2]/a/span'
        count_flwr = self.driver.find_element_by_xpath(flwer_x)
        count_flwr = count_flwr.get_attribute('title')

        # Number of scrolls in Follower window
        scrTimes = int(count_flwr) // 3
        sleep(sleep_time)

        # Locate and scroll the followers mini-window
        viewFollowers = '//section/main/div/header/section/ul/li[2]/a'
        sleep(sleep_time)
        viewFollowers = self.driver.find_element_by_xpath(
            viewFollowers).click()
        sleep(sleep_time)
        fBody = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        scroll = 0

        # Loop for scrolling
        while scroll < scrTimes:
            scrpt = """arguments[0].scrollTop = arguments[0].scrollTop
                                                + arguments[0].offsetHeight;"""
            self.driver.execute_script(scrpt, fBody)
            sleep(2)
            scroll += 1

        # Get a list of all the usernames (Followers)
        # Find relevant hrefs
        inViewHrefs = self.driver.find_elements_by_tag_name('a')
        inViewHrefs = [elem.get_attribute('title') for elem in inViewHrefs]
        f_list = []
        [f_list.append(title) for title in inViewHrefs if title not in f_list]

        # Remove first element, since it will always be ''
        del f_list[0]

        return f_list

    def file_work(self, new_f_list):
        """
        This method gets difference between old and new follower lists.
        This difference contains unfollower usernames.

        Arguments:
            new_f_list (list[str]):
                List of current followers.
        """
        newfSet = set(new_f_list)

        # Create "last_followers.txt" and "unfollowers.txt" if they don't exist
        if not os.path.exists('last_followers.txt'):
            with open('last_followers.txt', 'w'):
                pass
            with open('unfollowers.txt', 'w'):
                pass

        # Open and read the last_followers.txt file.
        with open('last_followers.txt', 'r+') as oldFileFlwr:
            oldf_list = [line.strip() for line in oldFileFlwr.readlines()]
        oldfSet = set(oldf_list)

        # Open and replace "last_followers.txt" file with new followers list
        with open('last_followers.txt', 'w') as newFileFlwr:
            for follower in newfSet:
                newFileFlwr.write(f'{follower}\n')

        # Get the usernames of people who no longer follow the user
        unfollowers = oldfSet.difference(newfSet)

        # Write them in "unfollowers.txt"
        dateChecked = datetime.now()
        with open('unfollowers.txt', 'a') as fileUnflwr:
            # If unfollowers list is empty
            if not unfollowers:
                fileUnflwr.write('No Unfollowers.\n')
            else:
                for unfollower in unfollowers:
                    print(f'The user "{unfollower}" no longer follows you.')
                    fileUnflwr.write(f'{unfollower}\n')
            fileUnflwr.write(f'STATS CHECKED: {dateChecked}\n\n')
