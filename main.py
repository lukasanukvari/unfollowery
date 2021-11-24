from bot import UnfollowersBot
import json


def main():
    with open('client_secret.json', 'r') as f:
        secret = json.load(f)
        un = secret['username']
        pwd = secret['password']

    UnfollowersBot(username=un, password=pwd)


if __name__ == '__main__':
    main()
