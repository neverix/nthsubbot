import praw


class Reddit:
    def __init__(self, name):
        self.reddit = praw.Reddit(name)
