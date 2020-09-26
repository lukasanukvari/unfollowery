from stats_bot import InstaBot, sleepTime
from datetime import datetime
from time import sleep
import os

class SmarterBot(InstaBot):
    """
    SmarterBot class (inherited) is for getting usernames of unfollowers.
    (The people, who has unfollowed the user)
    SmarterBot uses fileWork method to get the unfollowers.

    Arguments:
        username:str: The Instagram user's username.
        password:str: The Instagram user's password.

    Attributes:
        driver:Selenium.webdriver.Chrome:
            The driver of Chrome to automate its actions.
    """
    def __init__(self, username, password):
        super().__init__(username, password)
        sleep(sleepTime)
        self.driver.get(f'https://www.instagram.com/{username}/')
        sleep(sleepTime)
        scrTimes = int(self.followers) // 3 #Number of scrolls in Follower window.
        sleep(sleepTime)
        
        #Locate and scroll the followers mini-window.
        viewFollowers = '//section/main/div/header/section/ul/li[2]/a'
        sleep(sleepTime)
        viewFollowers = self.driver.find_element_by_xpath(viewFollowers).click()
        sleep(sleepTime)
        fBody  = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        scroll = 0
        while scroll < scrTimes: #Loop for scrolling.
            scrpt = 'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;'
            self.driver.execute_script(scrpt, fBody)
            sleep(2)
            scroll += 1

        #Get a list of all the usernames (Followers).
        inViewHrefs = self.driver.find_elements_by_tag_name('a') #Find relevant hrefs.
        inViewHrefs = [elem.get_attribute('title') for elem in inViewHrefs]
        fList = []
        [fList.append(title) for title in inViewHrefs if title not in fList]
        del fList[0] #Remove first element, since it will always be ''.
        
        self.fileWork(fList)
        self.driver.close()

    def fileWork(self, newfList):
        """
        This method gets difference between old and new follower lists.
        This difference contains unfollower usernames.

        Arguments:
            newfList:List:str: List of current followers.
        """
        newfSet = set(newfList)

        #Create "last_followers.txt" and "unfollowers.txt" if they don't exist.
        if not os.path.exists('last_followers.txt'):
            with open('last_followers.txt', 'w'):
                pass
            with open('unfollowers.txt', 'w'):
                pass

        #Open and read the last_followers.txt file.
        with open('last_followers.txt', 'r+') as oldFileFlwr:
            oldfList = [line.strip() for line in oldFileFlwr.readlines()]
        oldfSet = set(oldfList)

        #Open and replace the last_followers.txt file with new followers list.
        with open('last_followers.txt', 'w') as newFileFlwr:
            for follower in newfSet:
                newFileFlwr.write(f'{follower}\n')

        #Get the usernames of people who no longer follow the user.
        unfollowers = oldfSet.difference(newfSet)

        #Write them in unfollowers.txt.
        dateChecked = datetime.now()
        with open('unfollowers.txt', 'a') as fileUnflwr:
            if not unfollowers: #If unfollowers list is empty.
                fileUnflwr.write('No Unfollowers.\n')
            else:
                for unfollower in unfollowers:
                    print(f'The user "{unfollower}" no longer follows you.')
                    fileUnflwr.write(f'{unfollower}\n')
            fileUnflwr.write(f'STATS CHECKED: {dateChecked}\n\n')

if __name__ == '__main__':
    mainBot = SmarterBot('USERNAME', 'PASSWORD')
