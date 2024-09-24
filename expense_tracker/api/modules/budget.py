import frappe
from frappe import _
from expense_tracker.api.api_utils import remove_default_fields
from expense_tracker.api.models import BudgetModel


class Budget:
    def __init__(self):
        self.user = frappe.session.user

    def get_budget():
        """Retrieve all budgets"""
        budget = remove_default_fields(
            frappe.get_all(
                "Budget", filters={"user": frappe.session.user}, fields=["*"]
            )
        )
        frappe.response["message"] = "Budget list get successfully"
        return budget

    def create_budget(data: BudgetModel):
        pass

    def update_budget():
        pass
