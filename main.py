import praw  # reddit API
import db  # database access


def login():
    return praw.Reddit("nthsubbot")





if __name__ == '__main__':
    # log in
    reddit = login()
    # read the database
    db = db.DB("db.csv")
    # print contents
    db.print_contents()
