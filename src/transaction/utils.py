import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def get_month_name_from_number(month_number):
    """Returns the month name given a month number.
    Args:
        month_number: An integer.
    Returns:
        A string with the month name.
    """
    month = datetime.date(1900, month_number, 1).strftime("%B")
    return month


def send_account_summary_email(context):
    """Send an email with the account summary information."""
    plaintext = get_template("email.txt")
    htmly = get_template("email.html")

    subject, from_email, to = (
        "Account summary",
        "no-reply@stori.com",
        "customer@email.com",
    )
    text_content = plaintext.render(context)
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
