import pandas as pd  # working with tables


# Nth sub database
class DB:
    # create database from CSV file
    def __init__(self, path="db.csv"):
        self.db = pd.read_csv("db.csv")

    # print contents of database
    def print_contents(self):
        print(self.db)
