import frappe
from frappe import _
from expense_tracker.api.models import (
    TransactionModel,
    SavingTransactionModel,
    TransferTransactionModel,
    UpdateTransactionModel,
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

    def update_transaction(self, data: UpdateTransactionModel):
        """this will update all types of transaction"""
        transaction_type_map = {
            "Transaction": "Transaction",
            "Transfer Transaction": "Transfer Transaction",
            "Saving Transaction": "Saving Transaction",
        }

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

    def create_transfer_transaction(self, data: TransferTransactionModel):
        transfer_data = {
            "doctype": "Transfer Transaction",
            "user": frappe.session.user,
            "amount": data.amount,
            "transfer_type": data.transfer_type,
            "account_from": data.account_from,
            "account_to": data.account_to,
            "date": data.date,
            "location": data.location,
            "description": data.description,
            "recurring_transaction": data.recurring_transaction,
            "interval": data.interval,
            "recurring_date": data.recurring_date or None,
            "recurring_time": data.recurring_time or None,
        }
        if transfer_data.get('account_from') == transfer_data.get('account_to'):
            frappe.throw(("from account and to account can not be same !!"))
            
        if transfer_data["recurring_transaction"]:
            if not transfer_data.get("interval"):
                frappe.throw(_("Interval cannot be blank for a recurring transaction"))
            if transfer_data["interval"] == "Daily" and not transfer_data.get(
                "recurring_time"
            ):
                frappe.throw(_("Recurring Time cannot be blank for Daily interval"))

        transfer_doc = frappe.get_doc(transfer_data)

        if "receipt" in frappe.request.files:
            file = upload_file()
            file.update(
                {
                    "attached_to_doctype": transfer_doc.doctype,
                    "attached_to_name": transfer_doc.name,
                }
            )
            file.save(ignore_permissions=True)
            transfer_doc.receipt = file.file_url

        transfer_doc.insert(ignore_permissions=True)
        transfer_doc.save(ignore_permissions=True)

        frappe.response["message"] = "Transfer Transaction created successfully"
        frappe.response["transaction_id"] = transfer_doc.name

    def create_saving_transaction(self, data: SavingTransactionModel):
        saving_transaction_data = {
            "doctype": "Saving Transaction",
            "user": frappe.session.user,
            "amount": data.amount,
            "source_account": data.source_account,
            "date": data.date,
            "saving_goal": data.saving_goal,
        }
        saving_transaction_doc = frappe.get_doc(saving_transaction_data)

        saving_transaction_doc.insert(ignore_permissions=True)
        saving_transaction_doc.save(ignore_permissions=True)

        frappe.response["message"] = "Saving Transaction created successfully"
        frappe.response["transaction_id"] = saving_transaction_doc.name
