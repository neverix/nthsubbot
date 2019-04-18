import praw  # reddit API


def login():
    return praw.Reddit("nthsubbot")


if __name__ == '__main__':
    reddit = login()
    print(reddit.user.me())
