import frappe
from frappe import _
from expense_tracker.api.api_utils import remove_default_fields
from expense_tracker.api.models import BudgetModel


class Budget:
    def __init__(self):
        self.user = frappe.session.user

    def get_budget(self):
        """Retrieve all budgets"""
        budget = remove_default_fields(
            frappe.get_all(
                "Budget", filters={"user": frappe.session.user}, fields=["*"]
            )
        )
        frappe.response["message"] = "Budget list get successfully"
        return budget

    def create_budget(self,data: BudgetModel):
        """Create a new budget"""
        budget_doc = frappe.get_doc(
            dict(
                doctype="Budget",
                user=frappe.session.user,
                category=data.category,
                amount=data.amount,
            )
        )
        budget_doc.insert(ignore_permissions=True)
        frappe.response["message"] = "Budget created successfully"

    def update_budget(self, **data):
        """Update an existing Budget"""
        budget_doc = frappe.get_doc("Budget", data.get("budget"))
        
        if data.get("category"):
            budget_doc.category = data.get("category")
        if data.get("amount"):
            budget_doc.amount = data.get("amount")
            
        budget_doc.save(ignore_permissions=True)
        frappe.response["message"] = "Budget updated successfully"
