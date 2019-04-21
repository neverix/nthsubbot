import praw


# reddit API access
class Reddit:
    # log in
    def __init__(self, login_args):
        self.reddit = praw.Reddit(**login_args)

    # remove all posts and comments
    def remove_all(self):
        # get the user
        me = self.reddit.user.me()
        # remove comments
        for comment in me.comments.new():
            comment.delete()
        # remove posts
        for post in me.submissions.new():
            post.delete()
