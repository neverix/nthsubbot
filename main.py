import praw  # reddit API
import pandas as pd  # working with tables


def login():
    return praw.Reddit("nthsubbot")


if __name__ == '__main__':
    # log in
    reddit = login()
    # read the database
    db = pd.read_csv("db.csv")
    # print the database
    print(db)
