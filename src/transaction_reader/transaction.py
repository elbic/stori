import csv
import itertools
from collections import namedtuple

from .utils import group_by_kind, group_by_month, parse_date
from .exceptions import TransactionReaderFileError


class TransactionAmount:
    """Class to help identify the kind of transaction and it's amount.
    Attributes:
        transaction: A string containing the transaction amount and kind.
    """

    def __init__(self, transaction):
        """Inits the class casting the amount into float value and asigning  the
        amount kind."""
        self.amount = float(transaction)
        self.kind = "DEBIT" if self.amount < 0 else "CREDIT"

    def __repr__(self):
        """Class string representation."""
        return f"{self.kind}, {self.amount}"


class TransactionReader:
    """Class for reading and operate the transactions data in a CSV file."""

    def __init__(self, file_name):
        """Inits the TransactionReader class with the file_name and parser data
        types."""
        self.file_name = file_name
        self.parser = (int, parse_date, TransactionAmount)
        self.class_name = "Transaction"

    def csv_parser(self, *, delimiter=",", quotechar='"',
                   include_header=False):
        """Performs the reading of the CSV file.
        Returns:
            An iterator.
        """
        with open(self.file_name) as f:
            reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
            if not include_header:
                next(f)
            yield from reader

    def extract_field_names(self):
        """Extracts the CSV headers to use them as field names.
        Returns:
            A list with header names.
        """
        reader = self.csv_parser(include_header=True)
        return next(reader)

    def create_named_tuple_class(self):
        """Creates named tuples base on the field names.
        Returns:
            A named tuple.
        """
        fields = self.extract_field_names()
        return namedtuple(self.class_name, fields)

    def iterate_file(self):
        """Iterates over the CSV file skipping the header line.
        Returns:
            An iterator.
        """
        namedtuple_class = self.create_named_tuple_class()
        reader = self.csv_parser(include_header=False)
        for row in reader:
            parsed_data = (
                parser(value) for value, parser in zip(row, self.parser)
            )
            try:
                yield namedtuple_class(*parsed_data)
            except Exception as e:
                raise TransactionReaderFileError(e)

    def get_total_balance(self):
        """Computes the total balance in the CVS file.
        Returns:
            A float value representing the total balance in the CSV file.
        """
        data_iterable = self.iterate_file()
        return sum([item.Transaction.amount for item in data_iterable])

    def group_data(self, group_key):
        """Groups the data by the group_key function.
        Args:
            group_key: A function that returns the key to be group by.
        Returns:
            A list.
        """
        data_iterable = self.iterate_file()

        groups = sorted(
            (row for row in data_iterable), key=lambda x: group_key(x)
        )
        groups = itertools.groupby(groups, key=group_key)
        return groups

    def get_number_of_transactions(self):
        """Computes the number of transactions by mount.
        Returns:
            A list. For example:
            [(1, 2), (2, 1), (4, 2), (5, 1), (6, 2), (7, 3), (8, 1),
            (9, 1), (11, 4), (12, 3)]
        """
        groups = self.group_data(group_key=group_by_month)
        group_counts = ((g[0], len(list(g[1]))) for g in groups)
        return sorted(group_counts, key=lambda x: x[0])

    def get_average_amount(self):
        """Computes the average amount of transactions in the CSV file.
        Returns:
            A list. For example:
            [('CREDIT', 6518.909999999999), ('DEBIT', -3259.5899999999997)]
        """
        groups = self.group_data(group_key=group_by_kind)
        group_counts = (
            (g[0], sum([item.Transaction.amount for item in g[1]]))
            for g in groups
        )
        return sorted(group_counts, key=lambda x: x[0])

    # def get_average_amount_by_month(self):
    #     """Computes the number of transactions by mount.
    #     Returns:
    #     A dict. For example:
    #     {'DEBIT': [(1, -730.2), (7, -514.5699999999999), (9, -142.44),
    #     (11, -1741.29), (12, -131.09)], 'CREDIT': [(2, 207.4),
    #     (4, 623.68), (5, 423.29),
    #     (6, 1793.5), (7, 765.47), (8, 999.62), (11, 620.98), (12, 1084.97)]}
    #     """
    #     average_amount_by_month = dict()
    #     for kind in ('DEBIT', 'CREDIT', ):
    #         data_iterable = self.iterate_file()
    #
    #         groups = sorted((row for row in data_iterable if
    #         row.Transaction.kind == kind), key=lambda x: group_by_month(x))
    #         groups = itertools.groupby(groups, key=group_by_month)
    #         group_counts = ((g[0], sum(
    #         [item.Transaction.amount for item in g[1]])) for g in groups)
    #         average_amount_by_month[kind] = sorted(
    #         group_counts, key=lambda x: x[0])
    #     return average_amount_by_month
