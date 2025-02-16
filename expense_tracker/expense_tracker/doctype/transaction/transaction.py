# Copyright (c) 2024, Manav Mandli and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
from frappe.utils.background_jobs import enqueue
from datetime import datetime, timedelta


class Transaction(Document):
    def after_insert(self):
        self.update_account_details()
        self.update_budget()

    def update_account_details(self):
        if self.transaction_type == "Expense":
            account_doc = frappe.get_doc("User Account", self.account)
            account_doc.available_balance = flt(account_doc.available_balance) - flt(
                self.amount
            )
            account_doc.save()
        elif self.transaction_type == "Income":
            account_doc = frappe.get_doc("User Account", self.account)
            account_doc.available_balance = flt(account_doc.available_balance) + flt(
                self.amount
            )
            account_doc.save()

    def update_budget(self):
        if frappe.db.exists("Budget", {"user": self.user, "category": self.category}):
            budget_doc = frappe.get_doc(
                "Budget", {"user": self.user, "category": self.category}
            )
            budget_doc.spent_amount = flt(budget_doc.spent_amount) + flt(self.amount)
            budget_doc.save()
