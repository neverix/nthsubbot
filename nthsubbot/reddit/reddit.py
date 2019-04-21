""" Reddit API access. """

import praw
from typing import Tuple, Dict


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

    def post_or_edit(self, subreddits_posts: Dict[str, Tuple[str, str]]) -> Dict[str, str]:
        """
        Create or edit a submission to particular subreddits.
        :param subreddits_posts: mapping from subreddit to title and text of the post
        :return: the links to the posts
        """
        # links to the posts
        links = {}
        # subs that didn't get edited
        subs_left = list(subreddits_posts.keys())
        # loop over posts
        for post in self.reddit.user.me().submissions.new():
            # loop over subs
            for subreddit, (title, text) in subreddits_posts.items():
                # check if it's the post that we are looking for
                if post.subreddit.display_name == subreddit:
                    # edit it
                    post.edit(text)
                    # remove from the ones that didn't get edited
                    subs_left.remove(subreddit)
                    # add the link
                    links[subreddit] = post.url
        # loop over other subs
        for subreddit in subs_left:
            # get the title and text
            title, text = subreddits_posts[subreddit]
            # submit post
            post = self.reddit.subreddit(subreddit).submit(title, text)
            # add the link
            links[subreddit] = post.url
        return links
