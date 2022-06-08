import string
import os
from django.core.management.base import BaseCommand
import csv

import random
import time


# https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime("%m/%d", time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, "%m/%d/%Y", prop)


class Command(BaseCommand):
    help = "Creates a CSV file with transaction data."

    def add_arguments(self, parser):
        parser.add_argument("transactions", nargs="?", type=int, default=100)

    def handle(self, *args, **options):
        """
        Creates a user and a country so can start to use the app
        """
        header = ["Id", "Date", "Transaction"]
        file_path = os.getcwd() + "/base/data/"
        file_name = (
            file_path
            + "".join(random.choice(string.ascii_letters) for i in range(10))
            + ".csv"
        )
        with open(file_name, "w", encoding="UTF8", newline="") as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            for row_item in range(options["transactions"]):
                transaction_date = random_date(
                    "1/1/1900", "12/31/1900", random.random()
                )
                kind = random.choice(["+", "-"])
                amount = round(random.uniform(1, 999), 2)
                data = [row_item, transaction_date, f"{kind}{amount}"]
                # write the data
                writer.writerow(data)
