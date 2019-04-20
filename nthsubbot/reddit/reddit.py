import praw


# reddit API access
class Reddit:
    # log in
    def __init__(self, login_args):
        self.reddit = praw.Reddit(**login_args)
