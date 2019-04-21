import sqlite3  # working with tables
import csv  # exporting to CSV
import pprint


# Nth sub database
class DB:
    # read database
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.db = self.connection.cursor()

    # print contents of database
    def print_contents(self):
        print('\n'.join(str(row) for row in self.db.execute("SELECT * FROM database LIMIT 10").fetchall()))

    # find subreddit names by number
    def get_nth_subs(self, number):
        # get the part after r/ but before the / for all subs with that number
        return [
            get_subreddit(url) for (url,) in
            self.db.execute("SELECT Subreddit FROM database WHERE Number = ?", number).fetchall()]

    # convert database to CSV
    def to_csv(self, output_path):
        # open CSV file
        with open(output_path, 'w') as csv_file:
            # create a CSV writer
            csv_writer = csv.writer(csv_file)
            # select all rows
            self.db.execute("SELECT * FROM database")
            # write column names
            csv_writer.writerow([desc[0] for desc in self.db.description])
            # loop over rows
            for row in self.db:
                # write each row
                csv_writer.writerow(row)

    # destructor
    def __del__(self):
        # close cursor
        self.db.close()
        # close connection
        self.connection.close()

    # search nthsubs
    def search_nth_subs(self, number_gt=None, number_lt=None, number_eq=None, tags=None):
        # arguments handling
        if tags is None:
            tags = []
        # create super complex query
        query = f"""
        SELECT * FROM database
        WHERE Number LIKE '%%'
        {' AND Number > ?' if number_gt is not None else ''}
        {' AND Number < ?' if number_lt is not None else ''}
        {' AND Number = ?' if number_eq is not None else ''}
        {' AND Tag LIKE ?' * len(tags)}"""
        # create super complex arguments
        args = []
        if number_gt is not None:
            args.append(number_gt)
        if number_lt is not None:
            args.append(number_lt)
        if number_eq is not None:
            args.append(number_eq)
        args += [f'%{tag}%' for tag in tags]
        # execute it
        self.db.execute(query, args)
        # return results
        return self.db.fetchall()


# get the subreddit part after r/ but before the /
def get_subreddit(url):
    return url.split("r/")[1].split("/")[0]
