from main import main
from time import sleep

# Schedule unfollowers check for every N hours
N = 1

if __name__ == '__main__':
    while True:
        main()
        sleep(N * 3600)
