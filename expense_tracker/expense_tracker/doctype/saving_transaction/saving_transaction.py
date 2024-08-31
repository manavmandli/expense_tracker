# Copyright (c) 2024, Manav Mandli and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class SavingTransaction(Document):
    def validate(self):
        self.update_account()
        self.update_saving()

    def update_account(self):
        account_doc = frappe.get_doc("User Account", self.source_account)
        account_doc.available_balance = flt(account_doc.available_balance) - flt(
            self.amount
        )
        account_doc.save()

    def update_saving(self):
        saving_doc = frappe.get_doc("Saving Goals", self.saving_goal)
        saving_doc.saved_amount = flt(saving_doc.saved_amount) + flt(self.amount)
        saving_doc.save()
