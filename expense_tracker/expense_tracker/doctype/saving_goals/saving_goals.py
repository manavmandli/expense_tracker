# Copyright (c) 2024, Manav Mandli and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SavingGoals(Document):
    def validate(self):
        if (self.saved_amount or 0) > (self.saving_amount or 0):
            frappe.throw("Your Saved Amount is More Than Saving Amount !!")
