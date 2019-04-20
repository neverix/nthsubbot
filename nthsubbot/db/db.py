import pandas as pd  # working with tables


# Nth sub database
class DB:
    # create database from CSV file
    def __init__(self, path):
        self.db = pd.read_csv(path)
        self.path = path

    # print contents of database
    def print_contents(self):
        print(self.db)

    # find subreddit names by number
    def get_nth_subs(self, number):
        return [
            get_subreddit(url)  # get the part after r/ but before the /
            for url in self.db[self.db["Number"] == str(number)]["Subreddit"].tolist()]  # for all subs with that number


# get the subreddit part after r/ but before the /
def get_subreddit(url):
    return url.split("r/")[1].split("/")[0]
