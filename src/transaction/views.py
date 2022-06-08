import glob

from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse
from django.template import loader

from transaction_reader import TransactionReader

from .models import Transaction
from .utils import get_month_name_from_number, send_account_summary_email


def index(request):
    """Function based view to show the list of files to be processed."""
    csv_files = glob.glob("/app/src/base/data/*.csv")
    template = loader.get_template("transaction/index.html")
    context = {
        "csv_files": csv_files,
    }
    return HttpResponse(template.render(context, request))


def process_csv(request):
    """Function based view to compute transactions in the selected CSV file."""
    transactions = TransactionReader(request.POST["csv_file_path"])
    total_balance = transactions.get_total_balance()

    # Human readable format for the number of transaction
    number_of_transactions = transactions.get_number_of_transactions()
    number_of_transactions = dict(
        (get_month_name_from_number(key), value)
        for key, value in number_of_transactions
    )

    # Human readable format for the average amount
    average_amount = transactions.get_average_amount()
    average_amount = dict((key, value) for key, value in average_amount)

    stori_logo_path = request.build_absolute_uri(
        staticfiles_storage.url("images/stori-logo.jpeg")
    )
    template = loader.get_template("transaction/process_csv.html")

    context = {
        "total_balance": total_balance,
        "number_of_transactions": number_of_transactions,
        "average_amount": average_amount,
        "stori_logo_path": stori_logo_path,
    }

    # Bulk store the transactions
    objs = list(
        Transaction(
            transaction_id=transaction.Id,
            date=transaction.Date,
            kind=transaction.Transaction.kind,
            amount=transaction.Transaction.amount,
        )
        for transaction in transactions.iterate_file()
    )
    try:
        objs = Transaction.objects.bulk_create(objs)
    except Exception:
        pass

    # Attempts to send the account summary information
    send_account_summary_email(context)

    return HttpResponse(template.render(context, request))
