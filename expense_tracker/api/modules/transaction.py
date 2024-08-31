import frappe
from expense_tracker.api.api_utils import remove_default_fields


def get_transaction():
    """this will get all types of transaction"""
    transaction = []

    # get all Transaction
    transaction_doc = remove_default_fields(
        frappe.get_all(
            "Transaction", filters={"user": frappe.session.user}, fields=["*"]
        )
    )
    transaction.append(transaction_doc)

    # get all Transfer Transaction
    transfer_transaction_doc = remove_default_fields(
        frappe.get_all(
            "Transfer Transaction", filters={"user": frappe.session.user}, fields=["*"]
        )
    )
    transaction.append(transfer_transaction_doc)

    # get all Saving Transaction
    saving_transaction_doc = remove_default_fields(
        frappe.get_all(
            "Saving Transaction", filters={"user": frappe.session.user}, fields=["*"]
        )
    )
    transaction.append(saving_transaction_doc)

    frappe.response["message"] = "Transaction list get successfully"
    return transaction


def update_transaction():
    """this will get all types of transaction"""
    pass


def create_transaction():
    pass


def create_transfer_transaction():
    pass


def create_saving_transaction():
    pass
