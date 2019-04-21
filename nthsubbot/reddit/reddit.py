""" Reddit API access. """

import praw
from typing import Iterator, Tuple


class Reddit:
    """ Reddit API access. """
    def __init__(self, login_args: dict):
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

    def post(self, subreddit: str, title: str, text: str):
        """
        Makes the initial post to a subreddit.
        :param subreddit: subreddit to post it
        :param title: title of the post
        :param text: text of the post
        """
        # get the sub
        sub = self.reddit.subreddit(subreddit)
        # post to the sub
        sub.submit(title, text)

    def edit(self, subreddits_new_texts: Iterator[Tuple[str, str]]):
        """
        Edit the newest submission of the user to the subreddit
        :param subreddits_new_texts: iterator of pairs (subreddit, new text for the post)
        """
        # loop over all posts
        for post in self.reddit.user.me().submissions.new():
            # loop over possible subreddits
            for subreddit, new_text in subreddits_new_texts:
                # check if the post is from that subreddit
                if str(post.subreddit) == subreddit:
                    # edit the post
                    post.edit(new_text)
