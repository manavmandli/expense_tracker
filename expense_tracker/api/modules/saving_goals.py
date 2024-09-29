import frappe
from frappe import _
from expense_tracker.api.api_utils import remove_default_fields
from expense_tracker.api.models import SavingGoalsModel


class SavingGoal:
    def __init__(self):
        self.user = frappe.session.user

    def get_saving_goals():
        """Retrieve all Saving goals."""
        saving_goals = remove_default_fields(
            frappe.get_all(
                "Saving Goals", filters={"user": frappe.session.user}, fields=["*"]
            )
        )
        frappe.response["message"] = "Saving Goals list get successfully"
        return saving_goals

    def create_saving_goals(self, data: SavingGoalsModel):
        """Create a new saving goals"""
        saving_doc = frappe.get_doc(
            dict(
                doctype="Saving Goals",
                user=frappe.session.user,
                saving_amount=data.saving_amount,
                reason=data.reason,
                targeted_date=data.targeted_date,
                category=data.category,
            )
        )
        saving_doc.insert(ignore_permissions=True)
        frappe.response["message"] = "Saving Goal created successfully"

    def update_saving_goals(self, **data):
        """Update an existing Saving goal"""
        saving_doc = frappe.get_doc("Saving Goals", data.get("saving_goal"))

        if data.get("saving_amount"):
            saving_doc.saving_amount = data.get("saving_amount")
        if data.get("reason"):
            saving_doc.reason = data.get("reason")
        if data.get("targeted_date"):
            saving_doc.targeted_date = data.get("targeted_date")
        if data.get("category"):
            saving_doc.category = data.get("category")

        saving_doc.save(ignore_permissions=True)
        frappe.response["message"] = "Saving Goal updated successfully"
