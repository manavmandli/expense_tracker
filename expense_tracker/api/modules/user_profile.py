import frappe
from frappe import _
from expense_tracker.api.api_utils import remove_default_fields
from expense_tracker.api.models import UserModel


class UserProfile:
    def __init__(self):
        self.user = frappe.session.user

    def get_user_profile():
        """Retrieve all user profile"""
        user_profile = remove_default_fields(
            frappe.get_all(
                "User", filters={"name": frappe.session.user}, fields=["*"]
            )
        )
        frappe.response["message"] = "User Profile Details get successfully"
        return user_profile

    def update_user_profile():
        pass