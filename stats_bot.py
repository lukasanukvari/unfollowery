from selenium.webdriver.common.keys import Keys
from utils.set_chrome import driver
from time import sleep
import os

# Set this regarding your internet/system speed.
sleepTime = 5

class InstaBot:
    """
    InstaBot class instance initializing.
    Call the login method - Authenticate the user with Instagram.
    Call the userStats method - Print stats of the given user.

    Arguments:
        username:str: The Instagram user's username.
        password:str: The Instagram user's password.

    Attributes:
        driver:Selenium.webdriver.Chrome:
            The driver of Chrome to automate its actions.
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = driver
        
        #Let's log in...
        self.login()
        sleep(sleepTime)
        self.userStats(username)

    def login(self):
        """
        The login method authenticates user with instagram.
        [No arguments]
        """
        self.driver.get('https://www.instagram.com/accounts/login/')
        sleep(sleepTime)
        
        #Find a Username box, make it empty and enter the username.
        elem = self.driver.find_element_by_name('username')
        elem.clear()
        elem.send_keys(self.username)

        #Find a Password box, make it empty and enter the password.
        elem = self.driver.find_element_by_name('password')
        elem.clear()
        elem.send_keys(self.password)
        elem.send_keys(Keys.RETURN) #Submit.

    def userStats(self, user):
        """
        Call userStats method to print the stats of the given user.

        Argument:
            user:str: The username of the profile to get stats from.
        """
        print(f'\nProfile: {user}')
        self.driver.get(f'https://www.instagram.com/{user}/')
        sleep(sleepTime)

        #The following section checks if the profile is private or public.
        #Prints the stats according to it.
        #There is a difference in public and private profiles:
        #Their Following/Followers' XPaths do not match.
        #But the XPaths of their Posts' are the same.
        try:
            priv_x = '//section/main/div/div/article/div[1]/div/h2'
            check_private = self.driver.find_element_by_xpath(priv_x)
            check_private = check_private.get_attribute('innerHTML')
        except:
            check_private = None
        posts_x = '//section/ul/li[1]/span/span'
        
        #To deal with the difference (See upper comments).
        if check_private == 'This Account is Private':
            flwer_x = '//section/ul/li[2]/span/span'
            flwin_x = '//section/ul/li[3]/span/span'
        else:
            flwer_x = '//section/ul/li[2]/a/span'
            flwin_x = '//section/ul/li[3]/a/span'
        
        #Find the number of followers, following and posts.
        flwer = self.driver.find_element_by_xpath(flwer_x)
        flwer = flwer.get_attribute('title')
        self.followers = flwer
        flwin = self.driver.find_element_by_xpath(flwin_x)
        flwin = flwin.get_attribute('innerHTML')
        self.following = flwin
        posts = self.driver.find_element_by_xpath(posts_x)
        posts = posts.get_attribute('innerHTML')
        self.posts = posts

        #Print stats.
        print(f'\tFollowers: {self.followers}')
        print(f'\tFollowing: {self.following}')
        print(f'\tPosts: {self.posts}\n')

        return int(self.followers)       

def menu(classobj):
    """
    Menu for Instagram bot user.

    Arguments:
        classobj:class:InstaBot: Object of InstaBot class.
    """
    question = '\nDo you want to get IG stats of someone? (y/n)\n'
    answer = input(question).lower()
    while answer != 'n':
        if answer != 'y':
            print('\nYour answer should only be "y"(Yes) or "n"(No).')
            answer = input(question).lower()
            continue
        usrnm = input('\nType username of the wanted user: ')
        try:
            classobj.userStats(usrnm)
        except:
            print('\nThere is no profile with such username.')
        answer = input(question).lower()
    print('\nOkay, see you next time...')
    classobj.driver.close()

if __name__ == '__main__':
    isTrue = False
    while not isTrue:
        un = input('Your Instagram username: ')
        pw = input('Your Instagram password: ')
        try:
            myBot = InstaBot(un, pw)
            isTrue = True
        except:
            print('Invalid username or password...')
            print('Please, try again.')
    menu(myBot)