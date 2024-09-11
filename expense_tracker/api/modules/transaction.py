import frappe
from frappe import _
from expense_tracker.api.models import (
    TransactionModel,
    SavingTransactionModel,
    TransferTransactionModel,
)
from expense_tracker.api.api_utils import remove_default_fields
from frappe.handler import upload_file


class Transaction:
    def __init__(self):
        self.user = frappe.session.user

    def get_transaction(self):
        """this will get all types of transaction"""
        if frappe.session.user == "Guest":
            frappe.throw(_("You must be logged in first"))

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
                "Transfer Transaction",
                filters={"user": frappe.session.user},
                fields=["*"],
            )
        )
        transaction.append(transfer_transaction_doc)

        # get all Saving Transaction
        saving_transaction_doc = remove_default_fields(
            frappe.get_all(
                "Saving Transaction",
                filters={"user": frappe.session.user},
                fields=["*"],
            )
        )
        transaction.append(saving_transaction_doc)

        frappe.response["message"] = "Transaction list get successfully"
        return transaction

    def update_transaction():
        """this will get all types of transaction"""
        pass

    def create_transaction(self, data: TransactionModel):
        if frappe.session.user == "Guest":
            frappe.throw(_("You must be logged in to create a transaction."))

        transaction_data = {
            "doctype": "Transaction",
            "user": frappe.session.user,
            "amount": data.amount,
            "transaction_type": data.transaction_type,
            "category": data.category,
            "account": data.account,
            "date": data.date,
            "location": data.location,
            "description": data.description,
            "recurring_transaction": data.recurring_transaction,
            "interval": data.interval,
            "recurring_date": data.recurring_date or None,
            "recurring_time": data.recurring_time or None,
        }
        if transaction_data["recurring_transaction"]:
            if not transaction_data.get("interval"):
                frappe.throw(_("Interval cannot be blank for a recurring transaction"))
            if transaction_data["interval"] == "Daily" and not transaction_data.get(
                "recurring_time"
            ):
                frappe.throw(_("Recurring Time cannot be blank for Daily interval"))

        transaction_doc = frappe.get_doc(transaction_data)

        if "receipt" in frappe.request.files:
            file = upload_file()
            file.update(
                {
                    "attached_to_doctype": transaction_doc.doctype,
                    "attached_to_name": transaction_doc.name,
                }
            )
            file.save(ignore_permissions=True)
            transaction_doc.receipt = file.file_url

        transaction_doc.insert(ignore_permissions=True)
        transaction_doc.save(ignore_permissions=True)

        frappe.response["message"] = "Transaction created successfully"
        frappe.response["transaction_id"] = transaction_doc.name

    def create_transfer_transaction():
        pass

    def create_saving_transaction():
        pass
