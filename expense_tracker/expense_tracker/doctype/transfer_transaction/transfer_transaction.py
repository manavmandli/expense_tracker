# Copyright (c) 2024, Manav Mandli and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class TransferTransaction(Document):
    def validate(self):
        self.update_account_details()

    def update_account_details(self):
        if self.transfer_type:
            account_from = frappe.get_doc("User Account", self.account_from)
            account_from.available_balance = flt(account_from.available_balance) - flt(
                self.amount
            )
            account_from.save()
            account_to = frappe.get_doc("User Account", self.account_to)
            account_to.available_balance = flt(account_to.available_balance) + flt(
                self.amount
            )
            account_to.save()
