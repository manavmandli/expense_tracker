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
            "recurring_date": data.recurring_date,
            "recurring_time": data.recurring_time,
        }
        if data.recurring_transaction:
            if not data.interval:
                frappe.throw(_("Interval can not be blank"))
            if data.interval == "Daily":
                if not data.recurring_time:
                    frappe.throw(_("Time Can not be blank"))
            else:
                frappe.throw(_("Date and Time Can not be Blank"))

        transaction_doc = frappe.get_doc(transaction_data)
        if "file" in frappe.request.files:
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

    def create_transfer_transaction():
        pass

    def create_saving_transaction():
        pass
