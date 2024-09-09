import frappe
from frappe.utils.background_jobs import enqueue
from datetime import datetime, date


def create_recurrence():
    transactions = frappe.get_all("Transaction", filters={"recurring_transaction": 1})
    transfers = frappe.get_all(
        "Transfer Transaction", filters={"recurring_transaction": 1}
    )
    all_transaction = transactions + transfers

    for transaction in all_transaction:
        transaction_doc = frappe.get_doc(transaction.doctype, transaction.name)
        if transaction_doc.interval == "Daily":
            process_transaction(transaction.doctype, transaction_doc, is_daily=True)
        elif transaction_doc.interval == "Weekly":
            process_transaction(transaction.doctype, transaction_doc, is_weekly=True)
        elif transaction_doc.interval == "Monthly":
            process_transaction(transaction.doctype, transaction_doc, is_monthly=True)


def process_transaction(
    doctype, transaction_doc, is_daily=False, is_weekly=False, is_monthly=False
):
    current_time = datetime.now().time()

    if is_daily and current_time >= transaction_doc.time:
        create_new_transaction(doctype, transaction_doc)
    elif (
        is_weekly
        and datetime.now().date().weekday() == transaction_doc.date.weekday()
        and current_time >= transaction_doc.time
    ):
        create_new_transaction(doctype, transaction_doc)
    elif (
        is_monthly
        and datetime.now().day == transaction_doc.date.day
        and current_time >= transaction_doc.time
    ):
        create_transaction(doctype, transaction_doc)


def create_transaction(doctype, transaction_doc):
    new_transaction = frappe.new_doc(doctype)
    new_transaction.user = transaction_doc.user
    new_transaction.is_recurrence = 1
    new_transaction.amount = transaction_doc.amount
    new_transaction.transaction_type = transaction_doc.transaction_type
    new_transaction.category = transaction_doc.category
    new_transaction.account = transaction_doc.account
    new_transaction.date = date.today()
    new_transaction.description = transaction_doc.description
    new_transaction.location = transaction_doc.location
    new_transaction.receipt = transaction_doc.receipt
    new_transaction.save()
    frappe.db.commit()


enqueue(create_recurrence)
