import praw


class Bot:
    def __init__(self, name):
        self.reddit = praw.Reddit(name)
