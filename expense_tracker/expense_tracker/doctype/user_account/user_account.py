# Copyright (c) 2024, Manav Mandli and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_last_day, today


class UserAccount(Document):
    def validate(self):
        self.update_balance()

    def update_balance(self):
        if self.is_new():
            if self.payable:
                self.opening_balance = -abs(self.opening_balance)
                self.available_balance = self.opening_balance
            else:
                self.available_balance = abs(self.opening_balance)

        if today() == get_last_day(today()):
            self.opening_balance = self.available_balance
