""" Reddit API access. """


import praw


class Reddit:
    """ Reddit API access. """
    def __init__(self, login_args):
        """
        Logs in.
        :param login_args: parameters for the log in, used by praw.Reddit()
        """
        self.reddit = praw.Reddit(**login_args)

    def remove_all(self):
        """ Removes all posts and comments. """
        # get the user
        me = self.reddit.user.me()
        # remove comments
        for comment in me.comments.new():
            comment.delete()
        # remove posts
        for post in me.submissions.new():
            post.delete()
