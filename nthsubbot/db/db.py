"""
SQLite database operations.
"""

import sqlite3
import csv
from typing import Tuple, Iterator, List, Optional
from .nthsub import NthSub


class DB:
    """ Nth sub database. """
    def __init__(self, path: str):
        """
        Opens the database.
        :param path: the path of the SQLite database file.
        """
        self.connection = sqlite3.connect(path)
        self.db = self.connection.cursor()

    def print_contents(self):
        """ Prints contents of the database. """
        print('\n'.join(','.join(row) for row in self.db.execute("SELECT * FROM database LIMIT 50").fetchall()))

    def to_csv(self, output_path: str):
        """
        Converts the database to CSV.
        :param output_path: the path of the output CSV file.
        """
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

    def __del__(self):
        """ Destructor, closes DB connection and cursor. """
        # close cursor
        self.db.close()
        # close connection
        self.connection.close()

    def search_nth_subs(self,
                        number_gt: Optional[int] = None,
                        number_lt: Optional[int] = None,
                        number_eq: Optional[int] = None,
                        tags: List[str] = None) -> Iterator[NthSub]:
        """
        Searches Nth subs in a database.
        :param number_gt: the output subs' numbers must be greater than this
        :param number_lt: the output subs' numbers must be less than this
        :param number_eq: the output subs' numbers must be equal to this
        :param tags: the output subs will have these tags
        :returns the list of subs that fit the criteria
        """
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
        args += [f'% {tag} %' for tag in tags]
        # execute it
        self.db.execute(query, args)
        # return results
        return map(nthsub_from_record, self.db)


def nthsub_from_record(record: Tuple[str, str, str]) -> NthSub:
    """
    Creates an nthsub from a DB record.
    :param record: the record that will be converted
    """
    return NthSub(record[0][1:-1].split(' '), record[2], record[1])

