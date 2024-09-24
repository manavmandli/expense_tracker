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

    def create_saving_goals():
        pass

    def update_saving_goals():
        pass
