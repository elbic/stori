import os
from django.test import TestCase
from transaction_reader import TransactionReader, TransactionReaderFileError


class TransactionReaderTest(TestCase):
    def setUp(self):
        file = os.getcwd() + "/transaction_reader/tests/transaction.csv"
        self.transaction = TransactionReader(file)

    def test_get_total_balance(self):
        assert self.transaction.get_total_balance() == 1335.36

    def test_get_number_of_transactions(self):
        number_of_transactions = [
            (2, 1),
            (3, 1),
            (6, 1),
            (7, 1),
            (8, 3),
            (9, 1),
            (10, 2),
            (11, 1),
        ]
        assert (
            self.transaction.get_number_of_transactions()
            == number_of_transactions
        )

    def test_get_average_amount(self):
        average_amount = [("CREDIT", 3268.59), ("DEBIT", -1933.23)]
        assert self.transaction.get_average_amount() == average_amount


class TransactionReaderErrorTest(TestCase):
    def setUp(self):
        file = os.getcwd() + "/transaction_reader/tests/transaction_error.csv"
        self.transaction = TransactionReader(file)

    def test_get_total_balance_raises_proper_exception(self):
        with self.assertRaises(TransactionReaderFileError):
            self.transaction.get_total_balance()

    def test_get_number_of_transactions_raises_proper_exception(self):
        with self.assertRaises(TransactionReaderFileError):
            self.transaction.get_number_of_transactions()

    def test_get_average_amount_raises_proper_exception(self):
        with self.assertRaises(TransactionReaderFileError):
            self.transaction.get_average_amount()
