import praw  # reddit API
import db  # database access


def login():
    return praw.Reddit("nthsubbot")


if __name__ == '__main__':
    # log in
    reddit = login()
    # read the database
    db = db.DB("db.csv")
    # get 80th subreddit
    print(db.get_nth_subs(80))
